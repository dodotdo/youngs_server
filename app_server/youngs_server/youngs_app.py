# -*- coding: utf-8 -*-
"""
HIMS INIT

Hotel Intelligent Management System from DODOTDO INC.
"""

from datetime import timedelta

import hashlib
import os
import redis
from .youngs_logger import Log

log = Log()
from flask import Flask
from flask_login import LoginManager
from .common.session import ItsdangerousSessionInterface
from .database import db, bcrypt
from .helpers.http_client import HTTPClient

login_manager = LoginManager(add_context_processor=False)
hash_mod = hashlib.sha1()
client_socket = HTTPClient('127.0.0.1', '/')

youngs_redis = redis.Redis(host='localhost', port=6379, db=0)

def create_app(config_filename='config.default.DevelopmentConfig'):
    app = Flask(__name__)
    app.config.from_object(config_filename)

    app.secret_key = app.config['SECRET_KEY']
    app.permanent_session_lifetime = timedelta(minutes=app.config['SESSION_ALIVE_MINUTES'])
    app.session_interface = ItsdangerousSessionInterface()
    # SOCKET
    # url = '127.0.0.1'
    # client_socket.connect((url, 8000))

    # logging module
    log_filepath = os.path.join(app.config['ROOT_DIR'], 'app_server/log')
    log.init(log_filepath=log_filepath, log_level=app.config['LOG_LEVEL'])
    log.info("CREATE HIMS APP : "+__name__)

    db.init_app(app)
    bcrypt.init_app(app)
    login_manager.init_app(app)

    from youngs_server.api.auth_controllers import api_auth
    from youngs_server.api.member_controllers import api_member
    from youngs_server.api.lecture_controllers import api_lecture
    from youngs_server.api.question_controllers import api_question

    app.register_blueprint(api_auth)
    app.register_blueprint(api_member)
    app.register_blueprint(api_lecture)
    app.register_blueprint(api_question)
    return app