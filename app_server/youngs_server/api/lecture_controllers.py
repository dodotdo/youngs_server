# -*- coding: utf-8 -*-

import sys
import os
import base64
import time as ptime
import traceback
import ast

from youngs_server.api.review_controllers import ReviewItemList
from youngs_server.common.errors import abort_if_lecture_not_exist
from youngs_server.helpers.image_helper import generate_image_url
from youngs_server.helpers.image_helper import save_json_image
from youngs_server.youngs_app import hash_mod, db
from youngs_server.youngs_app import log
from flask import Blueprint, jsonify, request, send_file, current_app
from flask_login import current_user
from werkzeug.utils import secure_filename

# decorator for decorator that wrap the __dict__ function of wrapper
from youngs_server.customlib.flask_restful import Resource, Api, reqparse, abort, marshal
from youngs_server.models.host_models import Lecture, Attend, Review, Member
from youngs_server.models.host_rest_fields import lecture_fields, lecture_list_fields, member_list_fields
from sqlalchemy.orm.exc import NoResultFound, MultipleResultsFound, FlushError
from flask_login import login_required
from sqlalchemy import asc, desc, and_
from youngs_server.youngs_app import youngs_redis
from config.constants import Constants

api_lecture = Blueprint('lecture', __name__, url_prefix='/api/lecture', static_folder='static', template_folder='templates')
lecture_rest = Api(api_lecture)


class LectureItemList(Resource):
    def __init__(self):
        self.lecture_post_parser = reqparse.RequestParser()
        self.lecture_post_parser.add_argument('title', location='json', required=True, type=str)
        self.lecture_post_parser.add_argument('description', location='json', required=True, type=str)
        self.lecture_post_parser.add_argument('type', location='json', required=True, type=str)
        self.lecture_post_parser.add_argument('img', location='json', required=True, type=str)

    @login_required
    def post(self):
        args = self.lecture_post_parser.parse_args()
        lecture = Lecture(
            member_id=current_user.id,
            title=args.title,
            description=args.description,
            type=args.type
        )
        if args.img is not None:
            img_filename = save_json_image('LECTURE_IMAGE_FOLDER', args.img)
            lecture.img_filename = img_filename
            lecture.img_url = generate_image_url('lecture', img_filename)

        db.session.add(lecture)
        member = Member.query.filter_by(id=current_user.id).one()
        member.lecture_num += 1

        db.session.commit()

        return marshal(lecture, lecture_fields['normal'], envelope='results')

    @login_required
    def get(self):
        """
        :return: lecture list
        """
        print('hi')
        order_by = request.args.get('order_by')
        num = request.args.get('num', default=10)
        type = request.args.get('type')
        start = request.args.get('start', default=0)
        is_live = request.args.get('is_live', type=bool)
        is_attended = request.args.get('is_attended', type=bool)
        is_teaching = request.args.get('is_teaching', type=bool)



        lecture_filter_query = []
        if type is not None:
            try:
                type = ast.literal_eval(type)
            except:
                abort(406, message="type wrong formed. it should be like type=['TOEIC','FREE']")
            lecture_filter_query.append(Lecture.type.in_(type))
        if is_live is not None:
            lecture_filter_query.append(Lecture.is_live == is_live)
        if is_teaching is not None:
            lecture_filter_query.append(Lecture.member_id == current_user.id)
        if is_attended is True:
            # sorry for durty code haha
            lecture_list = Lecture.query.outerjoin(Attend).filter(Attend.member_id == current_user.id)
            return marshal({'results': lecture_list}, lecture_list_fields['normal'])

        lecture_order_query = []
        if order_by is not None:
            if order_by == 'type':
                lecture_order_query.append(desc(Lecture.type))
            elif order_by == 'point':
                lecture_order_query.append(desc(Lecture.point_avg))
            lecture_order_query.append(desc(Lecture.register_timestamp))


        lecture_query = Lecture.query.filter(*lecture_filter_query).group_by(Lecture).\
            order_by(*lecture_order_query)

        lecture_list = lecture_query.offset(start).limit(num).all()
        return marshal({'results': lecture_list}, lecture_list_fields['normal'])

class LectureItem(Resource):

    @login_required
    def delete(self, lecture_id):
        """
        :return: lecture
        """
        abort_if_lecture_not_exist(lecture_id)
        lecture = Lecture.query.filter_by(id=lecture_id).one()
        db.session.delete(lecture)
        db.session.commit()

        member = Member.query.filter_by(id=current_user.id).one()
        member.lecture_num -= 1
        # redis_res = youngs_redis.srem(Constants.REDIS_YOUNGS_LECTURE_LIVE_KEY, lecture.id)
        # if redis_res == 0:
        #     log.error('chat.controllers.LectureItem.delete redis lecture id not eixsts')
        # else:
        #     # remove the lecture's members on the redis
        #     youngs_redis.delete(Constants.redis_witalkie_lecture_members_key(lecture.id))
        return jsonify({'results': 'success'})

    @login_required
    def get(self, lecture_id):
        """
        :return: lecture
        """
        level = request.args.get('level', default='normal')
        if level == 'normal':
            lecture = Lecture.query.filter_by(id=lecture_id).one()
        if level == 'review':
            lecture = Lecture.query.filter_by(id=lecture_id).one()
            lecture.review_list = Review.query.filter_by(lecture_id=lecture_id).all()

        if level == 'listener':
            lecture = Lecture.query.filter_by(id=lecture_id).one()
            res = youngs_redis.smembers(Constants.redis_youngs_live_lecture_listener_key(lecture_id))
            if res is not None:
                for each_listener in res:
                    listener_id = int(each_listener.decode('utf-8'))
                    if listener_id == lecture.member_id:
                        continue
                    lecture.listener = Member.query.filter_by(id=listener_id).one()

        if level == 'full':
            lecture = Lecture.query.filter_by(id=lecture_id).one()
            lecture.review_list = Review.query.filter_by(lecture_id=lecture_id).all()

            res = youngs_redis.smembers(Constants.redis_youngs_live_lecture_listener_key(lecture_id))
            if res is not None:
                for each_listener in res:
                    listener_id = int(each_listener.decode('utf-8'))
                    if listener_id == lecture.member_id:
                        continue
                    lecture.listener = Member.query.filter_by(id=listener_id).one()

        return marshal(lecture, lecture_fields[level], envelope='results')


class LectureLiveItem(Resource):

    @login_required
    def put(self, lecture_id):
        """
        :return: lecture
        """
        is_live = request.json.get('is_live')
        if is_live is None:
            abort(406, message="is_live attribute required")
        abort_if_lecture_not_exist(lecture_id)
        lecture = Lecture.query.filter_by(id=lecture_id).one()
        lecture.is_live = is_live
        db.session.commit()
        if is_live:
            redis_res = youngs_redis.sadd(Constants.REDIS_YOUNGS_LIVE_LECTURE_KEY, lecture.id)
            print(redis_res)
        else:
            redis_res = youngs_redis.srem(Constants.REDIS_YOUNGS_LIVE_LECTURE_KEY, lecture.id)
            print(redis_res)

        return marshal(lecture, lecture_fields['normal'], envelope='results')

class LectureAttendItem(Resource):

    @login_required
    def post(self, lecture_id):
        lecture = Lecture.query.filter_by(id=lecture_id).one()
        if lecture.is_live is False:
            abort(403, message="Lecture is closed")

        res = youngs_redis.smembers(Constants.redis_youngs_live_lecture_listener_key(lecture_id))
        print(current_user.id)
        print(lecture.member_id)
        if res is not None:
            for each_listener in res:
                listener = int(each_listener.decode('utf-8'))
                if Member.query.filter_by(id=listener).first() is None:
                    # User removed
                    youngs_redis.srem(Constants.redis_youngs_live_lecture_listener_key(lecture_id), listener)

                if current_user.id == lecture.member_id:
                    continue

                if listener != current_user.id and listener != lecture.member_id:
                    abort(409, message="Someone is already listening the lecture")

        if Attend.query.filter_by(member_id=current_user.id, lecture_id=lecture_id).first() is None:

            attend = Attend(
                member_id=current_user.id,
                lecture_id=lecture_id
            )
            db.session.add(attend)
            db.session.commit()
        youngs_redis.sadd(Constants.redis_youngs_live_lecture_listener_key(lecture_id), current_user.id)
        youngs_redis.expire(Constants.redis_youngs_live_lecture_listener_key(lecture_id), 600)

        return jsonify({'results': 'success'})

    @login_required
    def delete(self, lecture_id):
        abort_if_lecture_not_exist(lecture_id)
        res = youngs_redis.srem(Constants.redis_youngs_live_lecture_listener_key(lecture_id), current_user.id)
        if res:
            return jsonify({'results': 'success'})
        else:
            abort(403, message="not listening")

class LectureListenerItem(Resource):
    @login_required
    def get(self, lecture_id):
        lecture = Lecture.query.filter_by(id=lecture_id).one()
        res = youngs_redis.smembers(Constants.redis_youngs_live_lecture_listener_key(lecture_id))
        listener_list = []
        if res is not None:
            for each_listener in res:
                listener_id = int(each_listener.decode('utf-8'))
                listener_list.append(Member.query.filter_by(id=listener_id).one())
        print(listener_list)
        return marshal({'results': listener_list}, member_list_fields['normal'])


lecture_rest.add_resource(LectureItemList, '')
lecture_rest.add_resource(LectureItem, '/<lecture_id>')
lecture_rest.add_resource(LectureLiveItem, '/<lecture_id>/live')
lecture_rest.add_resource(LectureListenerItem, '/<lecture_id>/listener')
lecture_rest.add_resource(LectureAttendItem, '/<lecture_id>/attend')
lecture_rest.add_resource(ReviewItemList, '/<lecture_id>/review')
