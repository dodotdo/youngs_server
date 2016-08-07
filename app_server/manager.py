# -*- coding: utf-8 -*-

# manage.py
import os
import csv
import sys
import json
import random

from datetime import datetime

import requests

from config.constants import Constants
from coverage import coverage
from flask import current_app
from youngs_server.helpers.image_helper import save_json_image, generate_image_url
from youngs_server import app
from flask_migrate import Migrate, MigrateCommand
from flask_script import Shell, Manager, Server
from youngs_server.models.host_models import Member, Question, Review, Lecture
from youngs_server.youngs_app import db, youngs_redis
from youngs_server.common.time_util import today_obj, now_datetime

from youngs_server.youngs_app import log

app.config['RUN'] = False
manager = Manager(app)
migrate = Migrate()
migrate.init_app(app, db, directory="./migrations")
base_dir = os.path.dirname(os.getcwd())
config_dir = os.path.join(base_dir, 'app_server/config')

server = Server(host="0.0.0.0", port=8082)
manager.add_command('db', MigrateCommand)

@manager.command
def initall():
    createdb()
    initmember()
    initlecture()
    initquestion()
    initreview()
    initredis()
    return 'success'

@manager.command
def initmember():
    dummy_dir = os.path.join(config_dir, 'image', 'profile')
    with open(os.path.join(config_dir, 'member.json')) as data_file:
        member_list = json.load(data_file)
        for each_member in member_list:
            member = Member(
                email=each_member['email'],
                nickname=each_member['nickname']
            )
            member.hash_password(each_member['password'])
            img_path = os.path.join(dummy_dir, each_member['profile_img'])
            profile_base64 = get_image_base64(img_path)
            profile_filename = save_json_image('PROFILE_IMAGE_FOLDER', profile_base64)
            member.profile_filename = profile_filename
            member.profile_url = generate_image_url('profile', profile_filename)

            db.session.add(member)
        db.session.commit()


@manager.command
def initlecture():
    dummy_dir = os.path.join(config_dir, 'image', 'lecture')
    with open(os.path.join(config_dir, 'lecture.json')) as data_file:
        lecture_list = json.load(data_file)
        for each_lecture in lecture_list:
            lecture = Lecture(
                title=each_lecture['title'],
                member_id=each_lecture['member'],
                description=each_lecture['description'],
                type=each_lecture['type'],
                status=each_lecture['status']
            )
            img_path = os.path.join(dummy_dir, each_lecture['img'])
            profile_base64 = get_image_base64(img_path)
            img_filename = save_json_image('LECTURE_IMAGE_FOLDER', profile_base64)
            lecture.img_filename = img_filename
            lecture.img_url = generate_image_url('lecture', img_filename)
            db.session.add(lecture)

            member = Member.query.filter_by(id=each_lecture['member']).first()
            member.lecture_num += 1


        db.session.commit()


@manager.command
def initquestion():
    type_list =  ['TOEFL', 'TOEIC', 'INTERVIEW', 'OPIC', 'FREE', 'LIFE']
    with open(os.path.join(config_dir, 'question.json')) as data_file:
        question_list = json.load(data_file)
        for each_question in question_list:
            question = Question(
                content=each_question,
                type=type_list[int(random.random()*6)]
            )
            db.session.add(question)
        db.session.commit()


@manager.command
def initreview():
    with open(os.path.join(config_dir, 'review.json')) as data_file:
        review_list = json.load(data_file)
        for each_review in review_list:
            review = Review(
                content=each_review['content'],
                point=each_review['point'],
                member_id=each_review['member_id'],
                lecture_id=each_review['lecture_id']
            )
            db.session.add(review)
            lecture = Lecture.query.filter_by(id=each_review['lecture_id']).first()
            lecture.new_point(each_review['point'])

            member = Member.query.filter_by(id=lecture.member_id).one()
            member.new_point(each_review['point'])
        db.session.commit()

@manager.command
def createdb():
    db.init_app(app)
    db.create_all()

@manager.command
def initredis():
    # initialize redis
    p = youngs_redis.pipeline()
    for each_member in Member.query.all():
        p.set('member:'+each_member.email, {
            'id': each_member.id
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


import base64
import os

def get_image_base64(base_image_path, image_types=['jpg']):
    encoded_strings = {}
    if os.path.exists(base_image_path):
        img = base_image_path
        # Set up the dict.
        if img not in encoded_strings:
            encoded_strings[img]=None
        # Get the image's full path.
        image_path = os.path.join(base_image_path,img)
        # Read and encode.
        with open(image_path, "rb") as stream:
            raw = stream.read()
            inc = base64.b64encode(raw)
            return 'data:image/png;base64,'+str(inc.decode('utf-8'))
        return encoded_strings
    else:
        print ('%s not found.' %base_image_path)

if __name__ == "__main__":
    manager.run()
