import os
from dateutil import tz
import datetime

class Config(object):
    APP_NAME = 'app_server'
    ROOT_DIR = os.path.dirname(os.getcwd())

    # HOTEL INFORMATION
    HOTEL_CHAIN = 'club'
    HOTEL_BRAND = 'beach&tennis'
    HOTEL_AREA = 'lajolla'
    HOTEL_NAME = 'ljbtc-host'

    RUN = True

    # VOICE
    ALLOWED_EXTENSIONS = set(['amr', 'mp3'])
    VERSION = '2.2.1dev'

    # ORACLE FILE
    ORACLE_ALLOWED_EXTENSIONS = set(['xml'])
    ORACLE_MAX_FILE_SIZE = 1024*1024
    ORACLE_UPLOAD_FOLDER = os.path.join(ROOT_DIR, APP_NAME, 'youngs_server', 'static', 'oracle/')

    #us main db
    # SQLALCHEMY_DATABASE_URI = 'postgresql://dodotdo:ektenekt25@youngs.cg8vtdazldqa.us-west-1.rds.amazonaws.com:5432'
    PERMANENT_SESSION_LIFETIME = datetime.timedelta(days=1)

    SQLALCHEMY_TRACK_MODIFICATIONS = False
    CSRF_ENABLED = True

    BASE_SERVER = 'http://ljbtc.hotelnyoungs.com'
    API_SERVER = BASE_SERVER +'/api'
    ONLINE_LAST_MINUTES = 5000
    SESSION_ALIVE_MINUTES = 60 * 24 * 30 * 60 # 60days
    SECRET_KEY = 'gi3mHUx8hcLoQrnqP1XOkSORrjxZVkST'
    GOOGLE_TRANSLATE_API_KEY = 'AIzaSyDwxPyclZAXE_sHjPYeixCY3BRZN9l6iRI'
    GCM_API_KEY = 'AIzaSyAWsnkrfJhBz2VkovdkAF6Ev95Zl6Y1Nis'
    STT_URL = 'https://stream.watsonplatform.net/speech-to-text/api/v1/sessions'
    STT_AUTH = 'cc451a67-dae9-4458-8c77-910ff5b69814'
    STT_KEY = '1l2zSWoXSQAV'

    # SOCKETIO
    SOCKETIO_REDIS_URL = 'redis://localhost:6379/0'

    # Celery
    CELERY_BROKER_URL = 'redis://localhost:6379/0'
    CELERY_RESULT_BACKEND = 'redis://localhost:6379/0'
    CELERY_ACCEPT_CONTENT = ['json', 'pickle']

    #floor divide quotient. for example 100 -> 101 is 1 floor
    FLOOR_DIV_QUOTIENT = 100
    STATIC_FOLDER = os.path.join(ROOT_DIR, APP_NAME, 'youngs_server', 'static')
    IMAGE_FOLDER= os.path.join(STATIC_FOLDER, 'image/')
    INROOM_WEBVIEW_FOLDER = os.path.join(STATIC_FOLDER, 'webview/')
    SIGNAGE_IMAGE_FOLDER = os.path.join(STATIC_FOLDER, 'image', 'signage/')
    ATTRACTION_IMAGE_FOLDER = os.path.join(STATIC_FOLDER, 'image', 'attraction/')
    SERVICE_IMAGE_FOLDER = os.path.join(STATIC_FOLDER, 'image', 'service/')
    HOTEL_IMAGE_FOLDER = os.path.join(STATIC_FOLDER, 'image', 'info/')
    VOICE_MSG_FOLDER= os.path.join(STATIC_FOLDER, 'voice/')

    PROFILE_IMAGE_FOLDER= os.path.join(STATIC_FOLDER, 'profile/')
    LECTURE_IMAGE_FOLDER= os.path.join(STATIC_FOLDER, 'lecture/')

    MOVIE_FOLDER = os.path.join(STATIC_FOLDER, 'movie/')

    APP_DIR = os.path.join(ROOT_DIR, APP_NAME, 'youngs_server/')
    LOG_FOLDER = os.path.join(ROOT_DIR, APP_NAME)

    # Gmail credential folder
    CREDENTIALS_FOLDER= os.path.join(ROOT_DIR, APP_NAME, 'config/google/')
    GMAIL_CREDENTIALS_FOLDER = os.path.join(ROOT_DIR, APP_NAME, 'config/google/gmail')

    # THUMBNAIL size
    SIGNAGE_WEB_SIZE = 300, 256

    # UTC time controller
    # San diego : US/Pacific -8 hours from UTC time
    # 'US/Pacific' -8 hours from UTC time
    # 'Asia/Seoul' +9 hours from UTC time
    # 'US/East-Indiana' -5 hours from UTC time
    utc_dict = {
        'UTC': 0,
        'US/Pacific': -8,
        'Asia/Seoul': 9,
        'US/East-Indiana': -5
    }
    UTC_FROM = 'Asia/Seoul'
    UTC_ZONE = 'Asia/Seoul'
    UTC_DIF = utc_dict[UTC_ZONE]

    AUTOPLAY_CHANNEL = ['Emergency']

    # Swagger spec
    API_VERSION = '2.3.2'
    API_SPEC_URL = '/docs'
    DOCS_FOLDER = 'docs/swagger/'

class DevelopmentConfig(Config):
    SQLALCHEMY_DATABASE_URI = 'sqlite:////tmp/youngs_test.db'
    BASE_SERVER = 'http://192.168.1.100'
    API_SERVER = BASE_SERVER + '/api'
    ENTRY_SERVER = 'http://localhost'
    DEBUG = True
    LOG_LEVEL = 'info'
    MOD = 'DEV'

    utc_dict = {
        'UTC': 0,
        'US/Pacific': -8,
        'Asia/Seoul': 9,
        'US/East-Indiana': -5
    }
    UTC_FROM = 'Asia/Seoul'
    UTC_ZONE = 'Asia/Seoul'
    UTC_DIF = utc_dict[UTC_ZONE]
