# -*- coding: utf-8 -*-

import os
from flask import Flask, render_template, request, url_for


def print_settings(config):
    print '========================================================'
    print 'SETTINGS for YOUNGS APPLICATION'
    print '========================================================'
    for key, value in config:
        print '%s=%s' % (key, value)
    print '========================================================'


"""
def url_for_other_page(page):
    args = request.view_args.copy()
    args['page'] = page
    return url_for(request.endpoint, **args)
"""

def create_app(config_filepath='resource/config.cfg'):
    youngs_app = Flask(__name__)

    from youngs_server.youngs_config import YoungsConfig
    youngs_app.config.from_object(YoungsConfig)
    youngs_app.config.from_pyfile(config_filepath, silent=True)
    print_settings(youngs_app.config.iteritems())

    # 로그 초기화
    from youngs_server.youngs_logger import Log
    log_filepath = os.path.join(youngs_app.root_path,
                                youngs_app.config['LOG_FILE_PATH'])
    Log.init(log_filepath=log_filepath)

    # 데이터베이스 처리
    from photolog.database import DBManager
    db_filepath = os.path.join(photolog_app.root_path,
                               photolog_app.config['DB_FILE_PATH'])
    db_url = photolog_app.config['DB_URL'] + db_filepath
    DBManager.init(db_url, eval(photolog_app.config['DB_LOG_FLAG']))
    DBManager.init_db()

    # 뷰 함수 모듈은 어플리케이션 객체 생성하고 블루프린트 등록전에
    # 뷰 함수가 있는 모듈을 임포트해야 해당 뷰 함수들을 인식할 수 있음

    from photolog.controller import *

    from photolog.photolog_blueprint import photolog
    photolog_app.register_blueprint(photolog)

    # SessionInterface 설정.
    # Redis를 이용한 세션 구현은 cache_session.RedisCacheSessionInterface 임포트하고
    # app.session_interface에 RedisCacheSessionInterface를 할당
    from photolog.cache_session import SimpleCacheSessionInterface
    photolog_app.session_interface = SimpleCacheSessionInterface()

    # 공통으로 적용할 HTTP 404과 500 에러 핸들러를 설정
    photolog_app.error_handler_spec[None][404] = not_found
    photolog_app.error_handler_spec[None][500] = server_error

    # 페이징 처리를 위한 템플릿 함수
    photolog_app.jinja_env.globals['url_for_other_page'] = \
        url_for_other_page

    return photolog_app