# -*- coding: utf-8 -*-

import re
import time as ptime
import jwt
from random import shuffle
from youngs_server.helpers.image_helper import save_json_image, generate_image_url
from youngs_server.youngs_app import db, hash_mod, youngs_redis
from youngs_server.youngs_app import log
from flask import Blueprint, jsonify, request, current_app
from youngs_server.models.host_models import Question
from youngs_server.models.host_rest_fields import question_fields, question_list_fields
from sqlalchemy import asc, func, exc

from youngs_server.customlib.flask_restful import Resource, Api, reqparse, abort, marshal
from flask_login import login_required, current_user



api_question = Blueprint('question', __name__, url_prefix='/api/question')
question_rest = Api(api_question)

class QuestionItemList(Resource):
    """Question class that create question or read question list.

    """
    def __init__(self):
        self.question_post_parser = reqparse.RequestParser()
        self.question_post_parser.add_argument(
            'type',
            location='json', required=True,
            type=str,
        )
        self.question_post_parser.add_argument(
            'content',
            location='json', required=True,
            type=str,
        )

    def post(self):
        args = self.question_post_parser.parse_args()
        question = Question(
                type=args.type,
                content=args.content
        )
        db.session.add(question)
        db.session.commit()
        return marshal(question, question_fields, envelope='results')

    def get(self):
        question_type = request.args.get('type')
        if question_type is None:
            abort(406, message="type is required")

        question_list = Question.query.filter_by(type=question_type).order_by(Question.id).all()
        print(question_list)
        shuffle(question_list)
        print(question_list)

        return marshal({'results': question_list}, question_list_fields)

question_rest.add_resource(QuestionItemList, '')