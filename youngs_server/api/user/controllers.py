# -*- coding: utf-8 -*-

import sys
from youngs_server.database import db
from youngs_server.model import model_fields
from flask_restful import Resource, Api, reqparse, abort, marshal
from flask import Blueprint, session
from youngs_server.model.user import User
from youngs_server.common.decorator import token_required
from youngs_server.youngs_logger import Log

reload(sys)
sys.setdefaultencoding('utf-8')
apiUser = Blueprint('user', __name__, url_prefix='/api/users')
userRest = Api(apiUser)


class UserInfo(Resource):
    #회원가입 api

    def __init__(self):
        self.user_post_parser = reqparse.RequestParser()
        self.user_post_parser.add_argument(
            'email', dest='email',
            location='json', required=True,
            type=str,
            help='email of the user'
        )
        self.user_post_parser.add_argument(
            'nickname', dest='nickname',
            location='json', required=True,
            type=str,
            help='nickname of the user'
        )
        self.user_post_parser.add_argument(
            'password', dest='password',
            location='json', required=True,
            type=str,
            help='password of the user'
        )

    def post(self):
        """signup"""
        args = self.user_post_parser.parse_args()
        Log.info("aefafaefa")

        duplicateUser = db.session.query(User).filter_by(email = args.email).first()

        if duplicateUser is not None:
            return abort(201, message='duplicate user')

        signupUser = User(
                email=args.email,
                nickname = args.nickname,
                imageFileNameOriginal = None,
                fileName = None,
                fileSize = None,
                learnClassCnt = 0,
                point = 0,
                teachingClassCnt = 0
        )
        signupUser.hash_password(args.password)

        db.session.add(signupUser)
        db.session.commit()

        return marshal(signupUser, model_fields.user_fields, envelope='results')

    @token_required
    def get(self):
        """get user information"""

        userId = session['userId']

        userInfo = db.session.query(User).filter_by(userId=userId).first()

        if userInfo is None:
            return abort(402, message="invalid user id")

        return marshal(userInfo, model_fields.user_fields, envelope='results')

userRest.add_resource(UserInfo, '')