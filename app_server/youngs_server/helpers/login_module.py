
from flask_login import logout_user, login_user
from flask import current_app, abort, session
from youngs_server.youngs_app import login_manager, youngs_redis, log
from youngs_server.models.host_models import Member
import jwt

@login_manager.user_loader
def user_loader(id):
    member = Member.query.filter_by(id=id).first()
    if member is None:
        return None
    if member.is_authenticated:
        return member
    else:
        return None


@login_manager.request_loader
def request_loader(request):
    authorization_value = request.headers.get('Authorization')
    try:
        if request.args.get('token') is not None:
            token = request.args.get('token').replace('JWT ', '', 1)

        elif request.headers.get('Authorization') is not None:
            token = authorization_value.replace('JWT ', '', 1)

        else:

            raise ValueError('Authorization Required')

        userinfo = jwt.decode(token, current_app.config['SECRET_KEY'])
        print(token)
        redis_userid = youngs_redis.hget('auth:token:'+str(token), 'id')
        if redis_userid is None:
            current_app.log.info('redis expired :' + token)
            raise jwt.ExpiredSignatureError
        # userid = redis_userid.decode('utf-8')
        # member = Member.query.filter_by(id=userid).first()
        # return member
        # if redis_userid.decode('utf-8') != userinfo['id']:)
        #     raise ValueError('Unauthorized')

    except jwt.ExpiredSignatureError:
        abort(401, 'Token Expired')
    except jwt.DecodeError:
        print('token format')
        abort(403, 'Wrong Token Format')
    except ValueError as e:
        print(e)
        abort(403, e)

    member = Member.query.filter_by(id=userinfo['id']).first()
    if member is None:
        print("member not exists")
        abort(403, 'Member not exists')

    login_user(member)
    return member


@login_manager.unauthorized_handler
def unauthorized_handler():
    return abort(403, 'Unauthorized')


def current_id(request):
    authorization_value = request.headers.get('Authorization')
    token = authorization_value.replace('JWT ', '', 1)
    userinfo = jwt.decode(token, current_app.config['SECRET_KEY'])
    if 'id' in userinfo:
        return userinfo['id']
    else:
        return None
