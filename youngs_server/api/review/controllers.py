# -*- coding: utf-8 -*-

import sys
from youngs_server.database import dbManager
from youngs_server.model import model_fields
from flask_restful import Resource, reqparse, marshal
from flask import session, request
from youngs_server.model.Review import Review
from youngs_server.common.decorator import token_required
from youngs_server.common.Util import dateToString
from youngs_server.api.channel.controllers import channelRest

reload(sys)
sys.setdefaultencoding('utf-8')


class Review(Resource):
    def __init__(self):
        self.review_post_parser = reqparse.RequestParser()
        self.review_post_parser.add_argument(
            'rate', dest='rate',
            location='json', required=True,
            type=float,
            help='review rate'
        )
        self.review_post_parser.add_argument(
            'review', dest='review',
            location='json', required=True,
            type=str,
            help='review'
        )
        self.review_post_parser.add_argument(
            'upload_date', dest='uploadDate',
            location='json', required=True,
            type=dateToString,
            help='review upload date'
        )

    @token_required
    def post(self, channelId):
        """ save review """
        args = self.review_post_parser.parse_args()
        reviewObj = Review(
            userId=session['userId'],
            rate=args.rate,
            review=args.review,
            uploadDate=args.uploadDate,
            channelId=channelId
        )

        dbManager.add(reviewObj)
        dbManager.commit()

        return marshal({'results': reviewObj}, model_fields.review_fields)


    @token_required
    def get(self, channelId):
        """ return review list depending on channel"""

        channelId = channelId
        reviewList = dbManager.query(Review).filter(channelId=channelId).all()

        return marshal({'results': reviewList}, model_fields.review_list_fields)

channelRest.add_resource(Review, '<channel_id>/review')