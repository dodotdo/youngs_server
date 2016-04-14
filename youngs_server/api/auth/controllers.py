# -*- coding: utf-8 -*-

import sys
from youngs_server.database import db
from youngs_server.model import model_fields
from flask_restful import Resource, Api, reqparse, abort, marshal
from flask import Blueprint, jsonify, request, session
from youngs_server.model.user import User
from youngs_server.youngs_logger import Log
from youngs_server.common.decorator import token_required

reload(sys)
sys.setdefaultencoding('utf-8')
apiAuth = Blueprint('loginOut', __name__, url_prefix='/api/auth')
authRest = Api(apiAuth)

class loginout(Resource) :
    def __init__(self):
        self.login_post_parser = reqparse.RequestParser()
        self.login_post_parser.add_argument(
            'userId', dest='notuse',
            location='json',
            type=int,
            help='id of user'
        )
        self.login_post_parser.add_argument(
            'email', dest='email',
            location='json', required=True,
            type=str,
            help='email of user'
        )
        self.login_post_parser.add_argument(
            'password', dest='password',
            location='json', required=True,
            type=str,
            help='password of user'
        )
        self.login_post_parser.add_argument(
            'token', dest='notuse',
            location='json',
            type=str,
            help='none'
        )
        self.login_post_parser.add_argument(
            'nickname', dest='notuse',
            location='json',
            type=str,
            help='nickname'
        )

    def post(self):
        """login"""

        args = self.login_post_parser.parse_args()

        requestEmail = args.email
        requestPassword = args.password

        user = db.session.query(User).filter_by(email=requestEmail).first()

        if user is None:
            Log.error('invalid email')
            return abort(401, message='unregisted user or invalid email')

        try:
            if not user.verify_password(requestPassword):
                Log.error('wrong password')
                return abort(401, message='wrong password')
        except:
            Log.error('login error')
            return abort(401, message='error')

        token = user.generate_auth_token()
        user.token = token
        session['token']= token
        session['userId']=user.userId
        Log.info(str(session['userId']))

        return marshal(user, model_fields.user_fields, envelope='results')

    @token_required
    def delete(self):
        """logout"""
        token = request.headers.get('Authorization')

        if token is None:
            Log.error('token is None')
            return jsonify({'message': 'token is None'})

        session['token']=None
        session['userId']=None

        return jsonify({'result': 'logout success'})

authRest.add_resource(loginout, '')