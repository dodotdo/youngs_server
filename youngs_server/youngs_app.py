# -*- coding: utf-8 -*-

import os
from flask import Flask


config_filepath='resource/config.cfg'
youngs_app = Flask(__name__)

#설정
from youngs_config import YoungsConfig
youngs_app.config.from_object(YoungsConfig)
youngs_app.config.from_pyfile(config_filepath, silent=True)

#시크릿 키
youngs_app.secret_key = youngs_app.config['SECRET_KEY']

# 로그
from youngs_logger import Log
log_filepath = os.path.join(youngs_app.root_path,
                                youngs_app.config['LOG_FILE_PATH'])
Log.init(log_filepath=log_filepath)

"""
# SessionInterface 설정.
# Redis를 이용한 세션 구현은 cache_session.RedisCacheSessionInterface 임포트하고
# app.session_interface에 RedisCacheSessionInterface를 할당
from cache_session import SimpleCacheSessionInterface
youngs_app.session_interface = SimpleCacheSessionInterface()
"""

from api.channel.controllers import apiChannel
from api.auth.controllers import apiAuth
from api.user.controllers import apiUser

youngs_app.register_blueprint(apiChannel)
youngs_app.register_blueprint(apiAuth)
youngs_app.register_blueprint(apiUser)


# 데이터베이스 처리
from database import db
db.init_app(youngs_app)

#db.drop_all()
#db.create_all()