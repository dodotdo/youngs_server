import sys
from youngs_server.database import db
from youngs_server.model import model_fields
from flask_restful import Resource, marshal, Api
from flask import session, jsonify
from youngs_server.model.user_channel import UserChannel
from youngs_server.model.channel import Channel
from youngs_server.common.decorator import token_required
from youngs_server.youngs_logger import Log

reload(sys)
sys.setdefaultencoding('utf-8')

class Listen(Resource):


    @token_required
    def put(self, channel_id):
        """ listen channel
        """
        userId = session['userId']

        userChannelModel = UserChannel(
            userId = userId,
            channelId = channel_id,
            type = 'd',
            isListening = True
        )

        listeningChannel = db.session.query(UserChannel).filter_by(userId = userId, isListening = True).first()

        #if user listen another channel
        if listeningChannel is not None :
            listeningChannel.isListening = False

        willListenChannel = db.session.query(UserChannel).filter_by(userId=userId, channelId = channel_id).first()

        #if user_channel is not exist
        if willListenChannel is None :
            #if channel is exist
            channel = db.session.query(Channel).filter_by(channelId = channel_id).first()
            if channel is not None :
                db.session.add(userChannelModel)
            else :
                return jsonify({'message': 'doesn`t exist'})
        else :
            willListenChannel.isListening = True

        db.session.commit()

        return marshal(userChannelModel, model_fields.user_channel_fields, envelope='results')

    @token_required
    def delete(self, channel_id):
        """listen out"""
        userId = session['userId']

        nowListeningChannel = db.session.query(UserChannel).filter_by(userId = userId, isListening = True, channelId = channel_id).first()

        #if user has not listen and channel is not exist
        if nowListeningChannel is None :
            Log.error('already not listening or doesn`t exist')
            return jsonify({'message': 'already not listening or doesn`t exist'})

        nowListeningChannel.isListening = False
        db.session.commit()

        return jsonify({'result': 'listen out success'})
