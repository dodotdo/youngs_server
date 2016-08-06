# -*- coding: utf-8 -*-

# manage.py
import os
import csv
import sys
from datetime import datetime

import requests

from config.constants import Constants
from coverage import coverage
from flask import current_app
from youngs_server.helpers.url_helper import generate_content_url
from youngs_server.helpers.url_helper import generate_image_url
from youngs_server import app
from flask_migrate import Migrate, MigrateCommand
from flask_script import Shell, Manager, Server
from youngs_server.models.host_models import Member
from youngs_server.youngs_app import db, youngs_redis
from youngs_server.common.time_util import today_obj, now_datetime

from youngs_server.youngs_app import log

app.config['RUN'] = False
manager = Manager(app)
migrate = Migrate()
migrate.init_app(app, db, directory="./migrations")


server = Server(host="0.0.0.0", port=8082)
manager.add_command('db', MigrateCommand)

@manager.command
def initall():
    createdb()
    initredis()
    
    return 'success'

@manager.command
def createdb():
    db.init_app(app)
    db.create_all()

@manager.command
def initredis():
    # initialize redis
    p = youngs_redis.pipeline()
    for each_member in Member.query.all():
        p.set('userid-'+each_member.email, {
            'email': each_member.email
        })
    p.execute()


@manager.command
def dropdb():
    app.config['RUN'] = False
    db.init_app(current_app)
    db.drop_all()
    sys.exit(0)


@manager.command
def run():
    manager.run()

if __name__ == "__main__":
    manager.run()
