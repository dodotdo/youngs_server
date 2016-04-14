# -*- coding: utf-8 -*-

import sys
from youngs_server.database import db
from youngs_server.model import model_fields
from flask_restful import Resource, reqparse, marshal
from flask import session
from youngs_server.model.review import Review
from youngs_server.common.decorator import token_required

reload(sys)
sys.setdefaultencoding('utf-8')


class ReviewInfo(Resource):
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
            type=str,
            help='review upload date'
        )

    @token_required
    def post(self, channel_id):
        """ save review """
        args = self.review_post_parser.parse_args()
        reviewObj = Review(
            userId=session['userId'],
            rate=args.rate,
            review=args.review,
            uploadDate=args.uploadDate,
            channelId=channel_id
        )

        db.session.add(reviewObj)
        db.session.commit()

        return marshal(reviewObj, model_fields.review_fields, envelope='results')


    @token_required
    def get(self, channel_id):
        """ return review list depending on channel"""

        reviewList = db.session.query(Review).filter_by(channelId=channel_id).all()

        return marshal({'results': reviewList}, model_fields.review_list_fields)
