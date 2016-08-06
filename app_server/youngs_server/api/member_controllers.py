# -*- coding: utf-8 -*-

import re
import time as ptime
import jwt
from youngs_server.helpers.image_helper import save_json_image, generate_image_url
from youngs_server.youngs_app import db, hash_mod, youngs_redis
from youngs_server.youngs_app import log
from flask import Blueprint, jsonify, request, current_app
from youngs_server.models.host_models import Member
from youngs_server.models.host_rest_fields import member_fields, member_list_fields
from sqlalchemy import asc, func, exc, desc
from youngs_server.common.errors import abort_if_member_email_not_exist, abort_if_member_email_exist
from youngs_server.customlib.flask_restful import Resource, Api, reqparse, abort, marshal
from flask_login import login_required, current_user



api_member = Blueprint('member', __name__, url_prefix='/api/member')
member_rest = Api(api_member)

class MemberItemList(Resource):
    """Member class that create member or read member list.

    """
    def __init__(self):
        self.member_post_parser = reqparse.RequestParser()
        self.member_post_parser.add_argument(
            'email',
            location='json', required=True,
            type=str,
        )
        self.member_post_parser.add_argument(
            'nickname',
            location='json', default='employed',
            type=str,
        )
        self.member_post_parser.add_argument(
            'password', 
            location='json', required=True,
            type=str,
        )
        self.member_post_parser.add_argument(
            'profile_img',
            location='json',
            type=str,
        )

    def post(self):
        args = self.member_post_parser.parse_args()
        email = args.email
        print(request.headers)
        if email is None:
            abort(406, message="needs email")
        if re.match("^[A-Za-z0-9._%+-]+@[A-Za-z0-9.-]+\.[A-Za-z]{2,}$", email) is None:
            abort(406, message="email wrong formatted")
        abort_if_member_email_exist(email)

        member = Member(
                email=email,
                nickname=args.nickname
        )
        member.hash_password(args.password)

        if args.profile_img is not None:
            print(args.profile_img)
            profile_filename = save_json_image('PROFILE_IMAGE_FOLDER', args.profile_img)
            member.profile_filename = profile_filename
            member.profile_url = generate_image_url('profile', profile_filename)

        db.session.add(member)
        db.session.commit()

        # Redis init
        p = youngs_redis.pipeline()
        for each_member in Member.query.all():
            log.info(each_member.email)
            p.set('member:'+each_member.email, {
                'id': each_member.id,
            })
        p.execute()
        return marshal(member, member_fields['normal'], envelope='results')

    def get(self):
        best_teacher = request.args.get('best_teacher')
        if best_teacher == 'true':
            member_list = Member.query.order_by(desc(Member.point_avg)).limit(3).all()
        else:
            member_list = Member.query.all()
        return marshal({'results': member_list}, member_list_fields['normal'])

member_rest.add_resource(MemberItemList, '')