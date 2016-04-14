# -*- coding: utf-8 -*-

import sys
from youngs_server.database import db
from youngs_server.model import model_fields
from flask_restful import Resource, reqparse, marshal
from flask import jsonify, session, request
from youngs_server.model.channel_info_from_user_channel import ChannelInfoModel
from youngs_server.model.user_channel import UserChannel
from youngs_server.model.review import Review
from youngs_server.model.channel import Channel
from youngs_server.youngs_logger import Log
from youngs_server.common.decorator import token_required

import datetime, time


reload(sys)
sys.setdefaultencoding('utf-8')

class UserChannelInfo(Resource):

    @token_required
    def get(self, channel_id):
        """return channel information in userchannel"""

        channelId = channel_id
        teacherId = request.args.get('teacherId')
        userId = session['userId']

        userChannelModel = UserChannel(
            userId = userId,
            channelId = channelId,
            type = 'd',
            isListening = False
        )

        nowListening = db.session.query(UserChannel).filter_by(channelId=channelId, isListening=True).all()
        favorite = db.session.query(UserChannel).filter_by(channelId=channelId, type="f").all()
        favoriteAndRead = db.session.query(UserChannel).filter_by(channelId=channelId, type="fr").all()
        read = db.session.query(UserChannel).filter_by(channelId=channelId, type="r").all()
        userChannel = db.session.query(UserChannel).filter_by(channelId=channelId, userId=userId).first()
        classCnt = db.session.query(Channel).filter_by(teacherId=teacherId).all()
        reviews = db.session.query(Review).filter_by(channelId=channelId).all()

        if userChannel is None:
            db.session.add(userChannelModel)
            userChannel = db.session.query(UserChannel).filter_by(channelId=channelId, userId=userId).first()

        isFavorite=False;
        isRead=False;

        if userChannel.type is "f" or userChannel.type is "fr" :
            isFavorite=True;

        if userChannel.type is "r" or userChannel.type is "fr" :
            isRead=True;


        reviewRate=0;
        for i in reviews:
            reviewRate += reviews[i].rate

        if len(reviews) is not 0 :
            reviewRate /= len(reviews)

        response = ChannelInfoModel(
            channelId = channelId,
            nowCnt = len(nowListening),
            favoriteCnt = len(favorite)+len(favoriteAndRead),
            readCnt = len(read)+len(favoriteAndRead),
            isFavorite = isFavorite,
            isRead = isRead,
            classCnt = len(classCnt),  #by teacher
            rate = reviewRate,
            reviewCnt = len(reviews)
        )

        return marshal(response, model_fields.user_channel_fields, envelope='results')

