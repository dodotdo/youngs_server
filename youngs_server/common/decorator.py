import ast
from datetime import date, time, datetime, timedelta
from dateutil import tz
from functools import wraps
from flask import current_app, jsonify, session, request
from youngs_server import database
from flask_restful import abort
from youngs_server.youngs_logger import Log


def token_required(f):
    """ token checking decoration """

    @wraps(f)
    def decorated_function(*args, **kwargs):
        # print session
        # temp

        token = request.headers.get('Authorization')
        print token
        if (token is None) or (len(token) < 7):
            abort(403, message='token invalid')

        token = token[6:]

        if token == '1':
            session['userId'] = -1
            session['token'] = '1'
            print session
        elif current_app.r.get(token) is None:
            Log.error('token invalid : token [' + token + ']')
            abort(403, message='token invalid')
        else:
            userinfo = ast.literal_eval(current_app.r.get(token))
            session['userId'] = userinfo['userId']
            session['token'] = token
        Log.info('token valid : user [' + session['userid'] + ']')
        return f(*args, **kwargs)

    return decorated_function
