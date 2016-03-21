# -*- coding: utf-8 -*-
"""
    photolog.blueprint
    ~~~~~~~~~~~~~~~~~~
    photolog 어플리케이션에 적용할 blueprint 모듈.
    :copyright: (c) 2013 by 4mba.
    :license: MIT LICENSE 2.0, see license for more details.
"""


from flask import Blueprint
from youngs_server.youngs_logger import Log

youngs = Blueprint('youngs', __name__,
                     template_folder='../templates', static_folder='../static')

Log.info('static folder : %s' % youngs.static_folder)
Log.info('template folder : %s' % youngs.template_folder)a