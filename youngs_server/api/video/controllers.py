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
            'teacherId', dest='teacherId',
            location='json', required=True,
            type=int,
            help='teacher id'
        )
        self.channel_post_parser.add_argument(
            'playtime', dest='playtime',
            location='json',
            type=int,
            help='youtube play time'
        )
        self.channel_post_parser.add_argument(
            'isPlaying', dest='isPlaying',
            location='json',
            type=bool,
            help='is playing or not'
        )


    @token_required
    def put(self, channel_id):
        """ set channel time information from teacher"""

        args = self.channel_post_parser.parse_args()
        nowVideoTime = db.session.query(VideoTime).filter_by(channelId=channel_id).first()

        newVideoTime = VideoTime(
            teacherId = args.teacherId,
            channelId = channel_id,
            playtime = args.playtime,
            updatedTime = datetime.datetime.now(),
            isPlaying = args.isPlaying
        )

        if nowVideoTime is None :
            db.session.add(newVideoTime)
            db.session.commit()
            Log.info('channel is now open')
            return marshal(newVideoTime, model_fields.video_time_fields, envelope='results')

        if session['userId'] == args.teacherId :
            nowVideoTime.playtime = args.playtime
            nowVideoTime.isPlaying = args.isPlaying

        nowVideoTime.updatedTime = datetime.datetime.now()

        db.session.commit()

        return marshal(nowVideoTime, model_fields.video_time_fields, envelope='results')


    @token_required
    def get(self, channel_id):
        """return channel time imformation"""

        nowVideoTime = db.session.query(VideoTime).filter_by(channelId=channel_id).first()

        if nowVideoTime is None :
            Log.error('invalid channel id')
            return jsonify({'message':'invalid channel id'})

        now = datetime.datetime.now()

        spaceTime = time.mktime(now.timetuple()) - time.mktime(nowVideoTime.updatedTime.timetuple())
        nowVideoTime.playtime += spaceTime

        nowVideoTime.updatedTime = now

        db.session.commit()

        return marshal(nowVideoTime, model_fields.video_time_fields, envelope='results')
