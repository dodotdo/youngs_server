# -*- coding: utf-8 -*-

import sys
from youngs_server.database import dbManager
from youngs_server.model import model_fields
from flask_restful import Resource, Api, reqparse, marshal
from flask import Blueprint, jsonify, session
from youngs_server.model.VideoTime import VideoTime
from youngs_server.youngs_logger import Log
from youngs_server.common.decorator import token_required

import time


reload(sys)
sys.setdefaultencoding('utf-8')
apiVideoTime = Blueprint('video_time', __name__, url_prefix='/api/video_time')
videoTimeRest = Api(apiVideoTime)


class VideoTimeInfo(Resource):
    # 채널 api

    def __init__(self):
        self.channel_post_parser = reqparse.RequestParser()
        self.channel_post_parser.add_argument(
            'teacher_id', dest='teacherId',
            location='json', required=True,
            type=int,
            help='channel id'
        )
        self.channel_post_parser.add_argument(
            'channel_id', dest='channelId',
            location='json', required=True,
            type=int,
            help='channel id'
        )
        self.channel_post_parser.add_argument(
            'now_youtube_time', dest='nowYoutubeTime',
            location='json',
            type=int,
            help='updated youtube time'
        )
        self.channel_post_parser.add_argument(
            'updated_time', dest='updateTime',
            location='json',
            type=int,
            help='time that update now_youtube_time'
        )
        self.channel_post_parser.add_argument(
            'is_playing', dest='isPlaying',
            location='json',
            type=bool,
            help='is playing or not'
        )


    @token_required
    def post(self):
        """ return channel time information"""

        args = self.channel_post_parser.parse_args()

        nowVideoTime = dbManager.__session.query(VideoTime).filter(channelId=args.channelId).first()

        newVideoTime = VideoTime(
            teacherId = args.teacherId,
            channelId = args.channelId,
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
        else :
            spaceTime = time.localtime() - nowVideoTime.updatedTime
            nowVideoTime.nowYoutubeTime += spaceTime


        nowVideoTime.updatedTime = newVideoTime.updatedTime

        dbManager.commit()

        return marshal({'results': newVideoTime}, model_fields.channel_fields)


videoTimeRest.add_resource(VideoTimeInfo, '')