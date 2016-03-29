# -*- coding: utf-8 -*-

import sys
from youngs_server.database import dbManager
from youngs_server.model import model_fields
from flask_restful import Resource, reqparse, marshal
from flask import jsonify, session
from youngs_server.model.VideoTime import VideoTime
from youngs_server.youngs_logger import Log
from youngs_server.common.decorator import token_required
from youngs_server.api.channel.controllers import channelRest

import time


reload(sys)
sys.setdefaultencoding('utf-8')

class VideoTimeInfo(Resource):
    # 채널 api

    def __init__(self):
        self.channel_post_parser = reqparse.RequestParser()
        self.channel_post_parser.add_argument(
            'teacher_id', dest='teacherId',
            location='json', required=True,
            type=int,
            help='teacher id'
        )
        self.channel_post_parser.add_argument(
            'now_youtube_time', dest='nowYoutubeTime',
            location='json',
            type=int,
            help='updated youtube time'
        )
        self.channel_post_parser.add_argument(
            'is_playing', dest='isPlaying',
            location='json',
            type=bool,
            help='is playing or not'
        )


    @token_required
    def put(self, channelId):
        """ set channel time information from teacher"""

        args = self.channel_post_parser.parse_args()

        nowVideoTime = dbManager.__session.query(VideoTime).filter(channelId=channelId).first()

        newVideoTime = VideoTime(
            teacherId = args.teacherId,
            channelId = channelId,
            nowYoutubeTime = args.nowYoutubeTime,
            updatedTime = time.localtime(),
            isPlaying = args.isPlaying
        )

        if nowVideoTime is None :
            dbManager.add(newVideoTime)
            dbManager.commit()
            Log.info('channel is now open')
            return jsonify({'message': 'channel is now open'})

        if session['userId'] == args.teacherId :
            nowVideoTime.nowYoutubeTime = args.nowYoutubeTime
            nowVideoTime.isPlaying = args.isPlaying


        nowVideoTime.updatedTime = newVideoTime.updatedTime

        dbManager.commit()

        return marshal({'results': nowVideoTime}, model_fields.channel_fields)


    @token_required
    def get(self, channelId):
        """return channel time imformation"""

        nowVideoTime = dbManager.__session.query(VideoTime).filter(channelId=channelId).first()

        if nowVideoTime is None :
            Log.error('invalid channel id')
            return jsonify({'message':'invalid channel id'}), 400

        spaceTime = time.localtime() - nowVideoTime.updatedTime
        nowVideoTime.nowYoutubeTime += spaceTime

        nowVideoTime.updatedTime = time.localtime()

        dbManager.commit()

        return marshal({'results': nowVideoTime}, model_fields.channel_fields)



channelRest.add_resource(VideoTimeInfo, '<channel_id>/video')