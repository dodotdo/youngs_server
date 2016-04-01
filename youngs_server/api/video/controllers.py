# -*- coding: utf-8 -*-

import sys
from youngs_server.database import db
from youngs_server.model import model_fields
from flask_restful import Resource, reqparse, marshal
from flask import jsonify, session
from youngs_server.model.video_time import VideoTime
from youngs_server.youngs_logger import Log
from youngs_server.common.decorator import token_required

import datetime, time


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
            'now_youtube_time_hour', dest='nowYoutubeTimeHour',
            location='json',
            type=int,
            help='updated youtube time hour'
        )
        self.channel_post_parser.add_argument(
            'now_youtube_time_minute', dest='nowYoutubeTimeMinute',
            location='json',
            type=int,
            help='updated youtube time minute'
        )
        self.channel_post_parser.add_argument(
            'now_youtube_time_second', dest='nowYoutubeTimeSecond',
            location='json',
            type=int,
            help='updated youtube time second'
        )
        self.channel_post_parser.add_argument(
            'is_playing', dest='isPlaying',
            location='json',
            type=bool,
            help='is playing or not'
        )


    @token_required
    def put(self, channel_id):
        """ set channel time information from teacher"""

        args = self.channel_post_parser.parse_args()
        Log.info("sefsefasafsfenebfkdrh")
        nowVideoTime = db.session.query(VideoTime).filter_by(channelId=channel_id).first()

        newVideoTime = VideoTime(
            teacherId = args.teacherId,
            channelId = channel_id,
            nowYoutubeTimeHour = args.nowYoutubeTimeHour,
            nowYoutubeTimeMinute = args.nowYoutubeTimeMinute,
            nowYoutubeTimeSecond = args.nowYoutubeTimeSecond,
            updatedTime = datetime.datetime.now(),
            isPlaying = args.isPlaying
        )

        if nowVideoTime is None :
            db.session.add(newVideoTime)
            db.session.commit()
            Log.info('channel is now open')
            return jsonify({'message': 'channel is now open'})

        if session['userId'] == args.teacherId :
            nowVideoTime.nowYoutubeTimeHour = args.nowYoutubeTimeHour
            nowVideoTime.nowYoutubeTimeMinute = args.nowYoutubeTimeMinute
            nowVideoTime.nowYoutubeTimeSecond = args.nowYoutubeTimeSecond
            nowVideoTime.isPlaying = args.isPlaying

        nowVideoTime.updatedTime = newVideoTime.updatedTime

        db.session.commit()

        return marshal(newVideoTime, model_fields.video_time_fields, envelope='results')


    @token_required
    def get(self, channel_id):
        """return channel time imformation"""

        nowVideoTime = db.session.query(VideoTime).filter_by(channelId=channel_id).first()

        if nowVideoTime is None :
            Log.error('invalid channel id')
            return jsonify({'message':'invalid channel id'})

        now = datetime.datetime.now()

        spaceTime = time.mktime(now.timetuple()) - time.mktime(nowVideoTime.updatedTime.timetuple())
        nowVideoTime.nowYoutubeTimeHour += spaceTime / 3600
        nowVideoTime.nowYoutubeTimeMinute += spaceTime / 60
        nowVideoTime.nowYoutubeTimeSecond += spaceTime % 60

        if nowVideoTime.nowYoutubeTimeSecond/60 >= 1 :
            tmpMin = nowVideoTime.nowYoutubeTimeSecond/60
            nowVideoTime.nowYoutubeTimeMinute += tmpMin
            nowVideoTime.nowYoutubeTimeSecond -= tmpMin*60

        if nowVideoTime.nowYoutubeTimeMinute/60 >= 1 :
            tmpHour = nowVideoTime.nowYoutubeTimeMinute/60
            nowVideoTime.nowYoutubeTimeHour += tmpHour
            nowVideoTime.nowYoutubeTimeMinute -= tmpHour*60

        nowVideoTime.updatedTime = now

        db.session.commit()

        return marshal(nowVideoTime, model_fields.video_time_fields, envelope='results')
