# -*- coding: utf-8 -*-

import sys
from youngs_server.database import dbManager
from youngs_server.model import model_fields
from youngs_server.common.Util import timeToString
from flask_restful import Resource, Api, reqparse, abort, marshal
from flask import Blueprint
from youngs_server.model.Channel import Channel

reload(sys)
sys.setdefaultencoding('utf-8')
apiMakeChannel = Blueprint('channel', __name__, url_prefix='/api/makeChannel')
makeChannelRest = Api(apiMakeChannel)


class MakeChannel(Resource):
    # 채널만들기 api

    def __init__(self):
        self.make_channel_post_parser = reqparse.RequestParser()
        self.make_channel_post_parser.add_argument(
            'title', dest='title',
            location='json', required=True,
            type=str,
            help='title of the channel'
        )
        self.make_channel_post_parser.add_argument(
            'description', dest='description',
            location='json', required=True,
            type=str,
            help='description of the channel'
        )
        self.make_channel_post_parser.add_argument(
            'teacher_id', dest='teacherId',
            location='json', required=True,
            type=int,
            help='teacher of the channel'
        )
        self.make_channel_post_parser.add_argument(
            'youtube_url', dest='youtubeURL',
            location='json', required=True,
            type=str,
            help='teacher of the channel'
        )
        self.make_channel_post_parser.add_argument(
            'is_free', dest='isFree',
            location='json', required=True,
            type=bool,
            help='channel is free or not'
        )
        self.make_channel_post_parser.add_argument(
            'teaching_day', dest='teachingDay',
            location='json', required=True,
            type=int,
            help='teachingDay of Channel, on-1, off-0'
        )
        self.make_channel_post_parser.add_argument(
            'teaching_start_time', dest='teachingStartTime',
            location='json', required=True,
            type=timeToString,
            help='teachingStartTime of Channel'
        )
        self.make_channel_post_parser.add_argument(
            'teaching_end_time', dest='teachingEndTime',
            location='json', required=True,
            type=timeToString,
            help='teachingEndTime of Channel'
        )
        self.make_channel_post_parser.add_argument(
            'price', dest='price',
            location='json', required=True,
            type=int,
            help='price of Channel free channel`s price is 0'
        )
        self.make_channel_post_parser.add_argument(
            'listening_limit_cnt', dest='listeningLimitCnt',
            location='json', required=True,
            type=int,
            help='limit count of person who listen Channel'
        )
        self.make_channel_post_parser.add_argument(
            'cover_image_file_name_original', dest='coverImageFileNameOriginal',
            location='json', type=str,
            help='limit count of person who listen Channel'
        )
        self.make_channel_post_parser.add_argument(
            'filename', dest='fileName',
            location='json', type=str,
            help='cover filename of channel'
        )
        self.make_channel_post_parser.add_argument(
            'filesize', dest='fileSize',
            location='json', type=int,
            help='cover filesize of channel'
        )

    def post(self):
        """makeChannel"""
        args = self.make_channel_post_parser.parse_args()

        duplicateChannel = Channel.query.filter_by(title=args.title).first()

        if duplicateChannel is not None:
            return abort(401, message='duplicate channel title')

        if args.coverImageFileNameOriginal is None:
            coverImageFileNameOriginal = ''
        else:
            coverImageFileNameOriginal = args.coverImageFileNameOriginal

        channel = Channel(
            title=args.title,
            description=args.description,
            teacherId=args.teacherId,
            youtubeURL=args.youtubeURL,
            isFree=args.isFree,
            teachingDay=args.teachingDay,
            teachingStartTime=args.teachingStartTime,
            teachingEndTime=args.teachingEndTime,
            price=args.price,
            listeningLimitCnt=args.listeningLimitCnt,
            coverImageFileNameOriginal=coverImageFileNameOriginal,
            fileName='',
            fileSize=0
        )

        dbManager.__session.add(channel)
        dbManager.__session.commit()

        return marshal(channel, model_fields.channel_fields, envelope='results')


makeChannelRest.add_resource(MakeChannel, '')
