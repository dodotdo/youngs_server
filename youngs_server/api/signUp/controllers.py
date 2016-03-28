# -*- coding: utf-8 -*-

import sys
from youngs_server.database import dbManager
from youngs_server.model import model_fields
from flask_restful import Resource, Api, reqparse, abort, marshal
from flask import Blueprint
from youngs_server.model.User import User

reload(sys)
sys.setdefaultencoding('utf-8')
apiSignup = Blueprint('signup', __name__, url_prefix='/api/signup')
signupRest = Api(apiSignup)


class UserSignup(Resource):
    #회원가입 api

    def __init__(self):
        #email, nickname, password
        self.signup_post_parser = reqparse.RequestParser()
        self.auth_post_parser.add_argument(
            'email', dest='email',
            location='json', required=True,
            type=str,
            help='email of the user'
        )
        self.auth_post_parser.add_argument(
            'nickname', dest='nickname',
            location='json', required=True,
            type=str,
            help='nickname of the user'
        )
        self.auth_post_parser.add_argument(
            'password', dest='pw',
            location='json', required=True,
            type=str,
            help='password of the user'
        )

    def post(self):
        """signup"""
        args = self.signup_post_parser.parse_args()

        duplicateUser = User.query.filter_by(nickname=args.nickname).first()

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

        dbManager.__session.add(signupUser)
        dbManager.__session.commit()

        return marshal(signupUser, model_fields.user_fields, envelope='results')




signupRest.add_resource(UserSignup, '')