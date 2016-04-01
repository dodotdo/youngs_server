# -*- coding: utf-8 -*-

class YoungsConfig(object):
    #: 데이터베이스 연결 URL
    SQLALCHEMY_DATABASE_URI= 'sqlite:////tmp/youngs.db'
    #: 데이터베이스 파일 경로
    DB_FILE_PATH= 'resource/database/youngs.db'
    #: 사진 업로드 시 사진이 임시로 저장되는 임시 폴더
    TMP_FOLDER = 'resource/tmp/'
    #: 업로드 완료된 사진 파일이 저장되는 폴더
    UPLOAD_CHANNEL_COVER_FOLDER = 'resource/channelcover/'
    #: 업로드되는 사진의 최대 크키(3메가)
    MAX_CONTENT_LENGTH = 10 * 1024 * 1024
    #: 세션 타임아웃은 초(second) 단위(60분)
    PERMANENT_SESSION_LIFETIME = 60 * 60
    #: 쿠기에 저장되는 세션 쿠키
    SESSION_COOKIE_NAME = 'youngs_session'
    #: 로그 레벨 설정
    LOG_LEVEL = 'debug'
    #: 디폴트 로그 파일 경로
    LOG_FILE_PATH = 'resource/log/youngs.log'
    #: 디폴트 SQLAlchemy trace log 설정
    DB_LOG_FLAG = 'True'
    #: 토큰 시크릿 키
    SECRET_KEY = 'aesfafaefaesfaew'
    #: 세션 유지 시간
    SESSION_ALIVE_MINUTES = 120