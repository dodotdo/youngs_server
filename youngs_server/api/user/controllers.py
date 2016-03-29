# -*- coding: utf-8 -*-

import sys
from youngs_server.database import dbManager
from youngs_server.model import model_fields
from flask_restful import Resource, Api, reqparse, abort, marshal
from flask import Blueprint, session
from youngs_server.model.User import User
from youngs_server.common.decorator import token_required

reload(sys)
sys.setdefaultencoding('utf-8')
apiUser = Blueprint('user', __name__, url_prefix='/api/users')
userRest = Api(apiUser)


class User(Resource):
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
            'password', dest='pw',
            location='json', required=True,
            type=str,
            help='password of the user'
        )

    def post(self):
        """signup"""
        args = self.user_post_parser.parse_args()

        duplicateUser = dbManager.query.filter_by(nickname=args.nickname).first()

        if duplicateUser is not None:
            return abort(401, message='duplicate user')

        signupUser = User(
                email=args.email,
                password = self.hash_password(args.pw),
                nickname = args.nickname,
                imageFileNameOriginal = None,
                fileName = None,
                fileSize = None,
                learnClassCnt = 0,
                point = 0,
                teachingClassCnt = 0
        )

        dbManager.add(signupUser)
        dbManager.commit()

        return marshal(signupUser, model_fields.user_fields, envelope='results')

    @token_required
    def get(self):
        """get user information"""

        userId = session['userId']

        userInfo = dbManager.query.filter_by(userId=userId).first()

        if userInfo is None:
            return abort(402, message="invalid user id")

        return marshal(userInfo, model_fields.user_fields, envelope='results')

userRest.add_resource(User, '')