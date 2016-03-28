# -*- coding: utf-8 -*-

import sys
from youngs_server.database import dbManager
from youngs_server.model import model_fields
from flask_restful import Resource, Api, reqparse, abort, marshal
from flask import Blueprint, session, request, jsonify
from youngs_server.model.UserChannel import UserChannel
from youngs_server.common.decorator import token_required
from youngs_server.youngs_logger import Log

reload(sys)
sys.setdefaultencoding('utf-8')
api = Blueprint('channelStatus', __name__, url_prefix='/api/channel_status')


@token_required
@api.route('/listen')
def startListen(self):
    if request.method == 'POST':
        channelId = request.json.get('channel_id')
        userId = session['userId']

        userChannelModel = UserChannel(
            userId = userId,
            channelId = channelId,
            type = request.json.get('type'),
            isListening = True
        )

        listeningChannel = dbManager.__session.query(UserChannel).filter(userId = userId, isListening = True).first()

        #다른방송을 듣고 있는경우
        if listeningChannel is not None :
            listeningChannel.isListening = False

        willListenChannel = dbManager.__session.query(UserChannel).filter(userId=userId, channelId = channelId).first()

        #db에 없는 경우
        if willListenChannel is None :
            dbManager.__session.add(userChannelModel)
        else :
            willListenChannel.isListening = True

        dbManager.__session.commit()

        return marshal({'results': userChannelModel}, model_fields.user_channel_fields)


@token_required
@api.route('/no_listen')
def endListen(self):
    if request.method == 'POST':
        channelId = request.json.get('channel_id')
        userId = session['userId']

        userChannelModel = UserChannel(
            userId = userId,
            channelId = channelId,
            type = request.json.get('type'),
            isListening = False
        )

        nowListeningChannel = dbManager.__session.query(UserChannel).filter(userId = userId, isListening = True, channelId = channelId).first()

        #수업을 듣고 있지 않은 경우 디비에 없는 경우
        if nowListeningChannel is None :
            Log.error('already not listening or doesn`t exist')
            return jsonify({'message': 'already not listening or doesn`t exist'}), 400

        nowListeningChannel.isListening = True
        dbManager.__session.commit()

        return marshal({'results': userChannelModel}, model_fields.user_channel_fields)

@token_required
@api.route('/change_status')
def changeStatus(self):
    if request.method == 'POST':
        channelId = request.json.get('channel_id')
        userId = session['userId']

        userChannelModel = UserChannel(
            userId = userId,
            channelId = channelId,
            type = request.json.get('type'),
            isListening = False
        )

        nowListeningChannel = dbManager.__session.query(UserChannel).filter(userId = userId, channelId = channelId).first()

        if nowListeningChannel is None :
            """디비에 없는 경우"""
            dbManager.__session.add(userChannelModel)
        else :
            """디비에 있는 경우"""
            nowListeningChannel.type = request.json.get('type')

        dbManager.__session.commit()

        return marshal({'results': userChannelModel}, model_fields.user_channel_fields)