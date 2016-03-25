# -*- coding: utf-8 -*-

import sys
from youngs_server.database import dbManager
from youngs_server.model import model_fields
from flask_restful import Resource, Api, reqparse, abort, marshal
from flask import Blueprint, session, request
from youngs_server.model.Review import Review
from youngs_server.common.decorator import token_required

reload(sys)
sys.setdefaultencoding('utf-8')
api = Blueprint('review', __name__, url_prefix='/api/')


@token_required
@api.route('review')
def postReview(self):
    if request.method == 'POST':
        reviewObj = Review(
            userId=session['userId'],
            rate=request.json.get('rate'),
            review=request.json.get('review'),
            uploadDate=request.json.get('upload_date'),
            channelId=request.json.get('channel_id')
        )

        dbManager.__session.add(reviewObj)
        dbManager.__session.commit()

        return marshal({'results': reviewObj}, model_fields.review_fields)


@api.route('review')
def getReviewList(self):
    """ return channel list depending on type"""

    if request.method == 'GET':
        channelId = request.args.get('channel_id')
        reviewList = dbManager.__session.query(Review).filter(channelId=channelId).all()

        return marshal({'results': reviewList}, model_fields.review_list_fields)
