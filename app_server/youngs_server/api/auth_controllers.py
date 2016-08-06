# -*- coding: utf-8 -*-

import jwt
from youngs_server.youngs_app import db, youngs_redis
from youngs_server.youngs_app import log
from youngs_server.customlib.flask_restful import Resource, Api, reqparse, abort, marshal
from datetime import datetime, timedelta
from flask import Blueprint, request, current_app, session, jsonify
from youngs_server.models.host_models import Member
from youngs_server.models.host_rest_fields import member_fields, auth_member_fields
from flask_login import login_user, login_required, logout_user

api_auth = Blueprint('auth', __name__, url_prefix='/api/auth')
auth_rest = Api(api_auth)

class MemberAuth(Resource):
    """Employee class that create employee or read employee list.
    """

    def __init__(self):
        self.auth_post_parser = reqparse.RequestParser()
        self.auth_post_parser.add_argument(
            'email',
            location='json', required=True,
            type=str,
        )
        self.auth_post_parser.add_argument(
            'password',
            location='json', required=True,
            type=str,
        )

    def post(self):
        """ login function """

        if 'application/json' in request.headers['Content-Type']:
            args = self.auth_post_parser.parse_args()
            email = args.email
            password = args.password

        else:
            raise abort(406, message='server cannot understand')
        # TODO get device type from headers

        member = Member.query.filter_by(email=email).one()

        if not member.verify_password(password):
            raise abort(401, message='id or pw is invalid')

        login_user(member)

        member.recent_login_timestamp = datetime.utcnow()
        db.session.commit()

        token_payload = {
            'email': member.email,
            'exp': datetime.utcnow() + timedelta(days=7)
        }
        token = jwt.encode(token_payload, current_app.config['SECRET_KEY'], algorithm='HS256').decode('utf-8')
        session_ttl = int(current_app.config['SESSION_ALIVE_MINUTES'] * 60)
        p = youngs_redis.pipeline()
        if youngs_redis.get('auth:token:'+token) is None:
            p.set('auth:token:'+token, member.email)
        p.expire('auth:token:'+token, session_ttl)
        p.execute()
        session['token'] = token
        member.token = token

        log.info('Login : '+member.email)

        return marshal(member, auth_member_fields, envelope='results')


    @login_required
    def delete(self):
        """
        :return: logout session, which means delete token and session
        """
        if 'token' in session:
            youngs_redis.get('auth:token:'+session['token'])
            log.info('session token %s', session['token'])
            youngs_redis.delete('auth:token'+session['token'])
        if 'user_id' in session:
            log.info('cleared session userid %s', session['user_id'])
        logout_user()
        return jsonify({'result': 'success'})



auth_rest.add_resource(MemberAuth, '/member')