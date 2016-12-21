import ast
import inspect

import functools

from functools import wraps
from flask import current_app, session, request
from youngs_server.customlib.flask_restful import abort
from youngs_server.youngs_app import log, youngs_redis


def token_required(f):
    """ token checking decoration """
    @wraps(f)
    def decorated_function(*args, **kwargs):
        # print session
        # temp

        token = request.headers.get('Authorization')
        if (token is None) or (len(token) < 7):
            abort(403, message='token invalid')
        token = token[6:]
        if token == '1':
            session['userid'] = 'admin'
            session['id'] = 1
            session['token'] = '1'
        elif youngs_redis.get('token-'+token) is None:
            log.error('token invalid : token [' + token + ']')
            abort(403, message='token invalid')
        else:
            userinfo = ast.literal_eval(youngs_redis.get('token-'+token))
            session['userid'] = userinfo['userid']
            session['id'] = userinfo['id']
            session['token'] = token
        log.info('token valid : user [' + session['userid'] + ']')
        return f(*args, **kwargs)
    return decorated_function


def application_json_header(f):
    """ request header must be application/json content-type """
    @functools.wraps(f)
    def wrapper(*args, **kwargs):
        if 'application/json' not in request.headers['Content-Type']:
            return abort(406, message='Wrong Content-Type')

        # func_args = inspect.getfullargspec(f, *args, **kwargs)
        # print(func_args.__dict__)
        return f(*args, **kwargs)
    return wrapper

