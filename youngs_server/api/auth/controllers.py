# -*- coding: utf-8 -*-

import sys
from youngs_server.database import dbManager
from youngs_server.model import model_fields
from flask_restful import Resource, Api, reqparse, abort, marshal
from flask import Blueprint, session, jsonify, current_app, request
from youngs_server.model.User import User
from youngs_server.youngs_logger import Log
from youngs_server.common.decorator import token_required

reload(sys)
sys.setdefaultencoding('utf-8')
authApi = Blueprint('loginOut', __name__, url_prefix='/api/auth')
authRest = Api(authApi)

class loginout(Resource) :
    def __init__(self):
        self.login_post_parser = reqparse.RequestParser()
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

    def post(self):
        """login"""

        args = self.login_post_parser.parse_args()

        requestEmail = args.email
        requestPassword = args.password

        user = dbManager.query(User).filter_by(email=requestEmail).first()

        if user is not None:
            Log.error('invalid email')
            return abort(401, message='unregisted user or invalid email')

        try:
            if not user.verify_password(requestPassword):
                Log.error('wrong password')
                return jsonify({'message': 'wrong password'}), 400
        except:
            Log.error('login error')

        token = user.generate_auth_token()

        session_ttl = int(current_app.config['SESSION_ALIVE_MINUTES'] * 60)
        p = current_app.r.pipeline()

        # logger : user login
        Log.info('login', user.userId + '/' + token)

        return marshal(user, model_fields.user_fields, envelope='results')

    @token_required
    def delete(self):
        """logout"""
        token = request.headers.get('Authorization')

        if token is None:
            Log.error('token is None')
            return jsonify({'message': 'token is None'}), 400

        token = token[6:]
        if current_app.r.get(token) is not None:
            current_app.r.delete(token)

        return jsonify({'result': 'logout success'})

authRest.add_resource(loginout, '')