# -*- coding: utf-8 -*-

import sys
from youngs_server.database import dbManager
from youngs_server.model import model_fields
from flask_restful import Resource, Api, reqparse, abort, marshal
from flask import Blueprint, session
from youngs_server.model.UserChannel import UserChannel
from youngs_server.common.decorator import token_required
from youngs_server.common.Util import dateToString


reload(sys)
sys.setdefaultencoding('utf-8')
apiReview = Blueprint('review', __name__, url_prefix='/api/review')
reviewRest = Api(apiReview)


class Review(Resource):
    # 리뷰 쓰기 or 리뷰 받기

    def __init__(self):
        self.review_post_parser = reqparse.RequestParser()
        self.review_post_parser.add_argument(
            'user_id', dest='userId',
            location='json', required=True,
            type=int,
            help='user id of user'
        )
        self.review_post_parser.add_argument(
            'rate', dest='rate',
            location='json', required=True,
            type=float,
            help='rate of review'
        )
        self.review_post_parser.add_argument(
            'review', dest='review',
            location='json', required=True,
            type=str,
            help='review text'
        )
        self.review_post_parser.add_argument(
            'upload_date', dest='uploadDate',
            location='json', required=True,
            type=dateToString,
            help='review upload date'
        )
        self.review_post_parser.add_argument(
            'channel_id', dest='channelId',
            location='json', required=True,
            type=int,
            help='review channel id'
        )

    def get(self):
        """ return channel list depending on type"""

        userId = session['userId']
        args = self.channel_post_parser.parse_args()
        channelList = dbManager.__session.query(UserChannel).filter(userId = userId, type=args.type).all()

        return marshal({'results': channelList}, model_fields.channel_list_fields)

reviewRest.add_resource(Review, '')
