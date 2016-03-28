# -*- coding: utf-8 -*-

import sys
from youngs_server.database import dbManager
from youngs_server.model import model_fields
from flask_restful import Resource, Api, reqparse, abort, marshal
from flask import Blueprint
from youngs_server.model.Channel import Channel


reload(sys)
sys.setdefaultencoding('utf-8')
apiChannelInfo = Blueprint('channel_info', __name__, url_prefix='/api/channel_info')
channelInfoRest = Api(apiChannelInfo)


class ChannelInfo(Resource):
    # 채널 api

    def __init__(self):
        self.channel_post_parser = reqparse.RequestParser()
        self.channel_post_parser.add_argument(
            'channel_id', dest='channelId',
            location='json', required=True,
            type=str,
            help='channel id'
        )


    def get(self):
        """ return channel information"""

        args = self.channel_post_parser.parse_args()

        channel = dbManager.__session.query(Channel).filter(channelId=args.channelId).first()

        if channel is None :
            return abort(401, message='channelId is not valid')

        return marshal({'results': channel}, model_fields.channel_fields)


channelInfoRest.add_resource(ChannelInfo, '')