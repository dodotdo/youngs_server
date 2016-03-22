# -*- coding: utf-8 -*-

from flask import Blueprint
from youngs_server.youngs_logger import Log

youngs = Blueprint('youngs', __name__, static_folder='../static')

Log.info('static folder : %s' % youngs.static_folder)