import sys
from youngs_server.database import dbManager
from youngs_server.model import model_fields
from flask_restful import Resource, Api, reqparse, abort, marshal
from flask import Blueprint, session, request, jsonify
from youngs_server.model.UserChannel import UserChannel
from youngs_server.common.decorator import token_required
from youngs_server.youngs_logger import Log
from youngs_server.api.channel.controllers import channelRest

reload(sys)
sys.setdefaultencoding('utf-8')

class Listen(Resource):


    @token_required
    def put(self, channelId):
        """ 수업듣기
        """
        userId = session['userId']

        userChannelModel = UserChannel(
            userId = userId,
            channelId = channelId,
            type = 'd',
            isListening = True
        )

        listeningChannel = dbManager.query(UserChannel).filter(userId = userId, isListening = True).first()

        #다른방송을 듣고 있는경우
        if listeningChannel is not None :
            listeningChannel.isListening = False

        willListenChannel = dbManager.query(UserChannel).filter(userId=userId, channelId = channelId).first()

        #db에 없는 경우
        if willListenChannel is None :
            dbManager.add(userChannelModel)
        else :
            willListenChannel.isListening = True

        dbManager.commit()

        return marshal({'results': userChannelModel}, model_fields.user_channel_fields)


    @token_required
    def delete(self, channelId):
        """수업나가기"""
        userId = session['userId']

        nowListeningChannel = dbManager.query(UserChannel).filter(userId = userId, isListening = True, channelId = channelId).first()

        #수업을 듣고 있지 않은 경우 디비에 없는 경우
        if nowListeningChannel is None :
            Log.error('already not listening or doesn`t exist')
            return jsonify({'message': 'already not listening or doesn`t exist'}), 400

        nowListeningChannel.isListening = True
        dbManager.commit()

        return jsonify({'result': 'listen out success'})

channelRest.add_resource(Listen, '<channel_id>/listen')