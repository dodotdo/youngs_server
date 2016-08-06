# -*- coding: utf-8 -*-

import re
import time as ptime
import jwt
from random import shuffle
from youngs_server.helpers.image_helper import save_json_image, generate_image_url
from youngs_server.youngs_app import db, hash_mod, youngs_redis
from youngs_server.youngs_app import log
from flask import Blueprint, jsonify, request, current_app
from youngs_server.models.host_models import Review, Lecture, Member
from youngs_server.models.host_rest_fields import review_fields, review_list_fields
from sqlalchemy import asc, func, exc
from youngs_server.common.errors import abort_if_lecture_not_exist
from youngs_server.customlib.flask_restful import Resource, Api, reqparse, abort, marshal
from flask_login import login_required, current_user


class ReviewItemList(Resource):
    """Review class that create review or read review list.

    """
    def __init__(self):
        self.review_post_parser = reqparse.RequestParser()
        self.review_post_parser.add_argument(
            'point',
            location='json', required=True,
            type=int,
        )
        self.review_post_parser.add_argument(
            'content',
            location='json', required=True,
            type=str,
        )

    def post(self, lecture_id):
        abort_if_lecture_not_exist(lecture_id)
        lecture = Lecture.query.filter_by(id=lecture_id).one()
        args = self.review_post_parser.parse_args()
        review = Review(
                lecture_id=lecture_id,
                member_id=current_user.id,
                point=args.point,
                content=args.content
        )
        lecture.new_point(args.point)

        member = Member.query.filter_by(id=lecture.member_id).one()
        member.new_point(args.point)
        db.session.add(review)
        db.session.commit()
        return marshal(review, review_fields, envelope='results')

    def get(self, lecture_id):
        abort_if_lecture_not_exist(lecture_id)
        review_list = Review.query.filter_by(lecture_id=lecture_id).all()
        return marshal({'results': review_list}, review_list_fields['normal'])
