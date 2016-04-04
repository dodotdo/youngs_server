from functools import wraps
from flask import session, request
from flask_restful import abort
from youngs_server.youngs_logger import Log
from youngs_server.model.user import User
from youngs_server.database import db


def token_required(f):
    """ token checking decoration """

    @wraps(f)
    def decorated_function(*args, **kwargs):
        # print session
        # temp

        token = request.headers.get('Authorization')

        if (token is None) or (len(token) < 7):
            abort(403, message='token invalid')

        userObj = User.verify_auth_token(token)
        session['userId'] = userObj.userId
        session['token'] = token
        Log.info('token valid : user [' + str(session['userId']) + ']')
        return f(*args, **kwargs)

    return decorated_function
