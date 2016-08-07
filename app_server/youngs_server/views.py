# -*- coding: utf-8 -*-

import time
import json

import jwt
import os
from youngs_server.customlib.flask_restful import abort
from sqlalchemy import exc
from werkzeug.exceptions import HTTPException
from . import app
from flask import render_template, Response, redirect, request, session, g, current_app, send_file, jsonify
from flask_login import current_user
from datetime import datetime
from youngs_server.youngs_app import db
from youngs_server.youngs_app import log


@app.route('/gmail/oauth2callback')
def oauth():
    print((request.headers))
    print((request.data))
    print('gmail')



@app.route('/res/image/signage/<filename>')
def get_signage_image(filename):
    try:
        return send_file(os.path.join(current_app.config['SIGNAGE_IMAGE_FOLDER'], filename))

    except HTTPException as e:
        log.error({"code": e.code, "description": e.description})
        raise
    except IOError as e:
        log.critical('voice file problem : ' + e)
        return jsonify({'message': 'IO Error'}), 404
    except exc.SQLAlchemyError as e:
        log.error({"code": e.code, "description": e.description})
        db.session.rollback()
        return abort(403, message='Wrong Token')
    except Exception as e:
        log.critical('Unexpected Error : ' + e)
        return jsonify({'message': str(e)}), 500


@app.after_request
def after_request_headers(response):
    response.headers.add('Access-Control-Allow-Origin', '*')
    response.headers.add('Access-Control-Allow-Headers', 'Origin, X-Atmosphere-tracking-id, Authorization, X-Atmosphere-Framework, X-Cache-Date, Content-Type, X-Atmosphere-Transport, *')
    # response.headers.add('Access-Control-Expose-Headers', "Authorization")
    response.headers.add('Access-Control-Request-Headers:', 'Origin, X-Atmosphere-tracking-id, X-Atmosphere-Framework, X-Cache-Date, Content-Type, X-Atmosphere-Transport,  *')

    response.headers.add('Access-Control-Allow-Methods', "GET, POST, PUT, DELETE, OPTIONS")
    response.headers.add('Access-Control-Allow-Credentials', "true")
    response.headers.add('Access-Control-Max-Age', 60 * 60 * 24 * 20)
    return response


# Automatically tear down SQLAlchemy
@app.teardown_request
def shutdown_session(exception= None):
    db.session.remove()

@app.before_request
def before_request():
    g.start = datetime.now()

@app.after_request
def after_request(response):
    request_args = {}
    for each_arg in request.args:
        request_args[each_arg] = request.args[each_arg]
    if 'text/html' in response.headers['Content-Type']:
        return response

    diff = datetime.now() - g.start
    try:
        authorization_value = request.headers.get('Authorization')
        token = authorization_value.replace('JWT ', '', 1)
        userinfo = jwt.decode(token, current_app.config['SECRET_KEY'])
        print(userinfo)
        request_log = {
            'id': current_user.id,
            'request_path': request.path,
            'request_args': request_args,
            'request_method': request.method,
            'response_time': diff,
            'response_status': response.status_code,
        }
    except Exception as e:
        print(e)
        log.error('Logging error')
        return response
    if app.config['LOG_LEVEL'] == 'debug' and 'json' in response.headers['Content-Type']:
        request_log['response_data'] = json.loads(response.data.decode('utf-8'))
    try:
        log.info('request log', extra=request_log)
    except Exception as e:
        log.error('Logging error : %s', e)

    return response

