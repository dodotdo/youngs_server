# -*- coding: utf-8 -*-

import logging
import logstash
import os
from pythonjsonlogger import jsonlogger

class Log:

    __log_level_map = {
        'debug' : logging.DEBUG,
        'info' : logging.INFO,
        'warn' : logging.WARN,
        'error' : logging.ERROR,
        'critical' : logging.CRITICAL
        }

    __youngs_logger = None

    @staticmethod
    def init(logger_name='youngs-logger',
             log_level='debug',
             log_filepath='app/log/youngs.log'):
        Log.__youngs_logger = logging.getLogger(logger_name)
        Log.__youngs_logger.setLevel(Log.__log_level_map.get(log_level, 'warn'))
        formatter = jsonlogger.JsonFormatter(
                '%(asctime) %(levelname) %(process) %(module) %(funcName) %(message)'
        )

        # logstashLogHandler = logstash.LogstashHandler(logger_name, 5959, version=1)
        if log_level == 'debug' or 'error':
            streamLogHandler = logging.StreamHandler()
            streamLogHandler.setFormatter(formatter)
            Log.__youngs_logger.addHandler(streamLogHandler)

        fileLogHandler = logging.handlers.TimedRotatingFileHandler(
                os.path.join(log_filepath, 'youngs_server.log'), when='D', interval=1)
        fileLogHandler.setFormatter(formatter)
        # Log.__youngs_logger.addHandler(logstashLogHandler)
        Log.__youngs_logger.addHandler(fileLogHandler)



    @staticmethod
    def debug(msg, *args, **kwargs):
        Log.__youngs_logger.debug(msg, *args, **kwargs)

    @staticmethod
    def info(msg, *args, **kwargs):
        Log.__youngs_logger.info(msg ,*args, **kwargs)

    @staticmethod
    def warn(msg, *args, **kwargs):
        Log.__youngs_logger.warn(msg, *args, **kwargs)

    @staticmethod
    def error(msg, *args, **kwargs):
        Log.__youngs_logger.error(msg, *args, **kwargs)

    @staticmethod
    def critical(msg, *args, **kwargs):
        Log.__youngs_logger.critical(msg, *args, **kwargs)



