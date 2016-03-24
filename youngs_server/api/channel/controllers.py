# -*- coding: utf-8 -*-

import sys
from youngs_server.database import dbManager
from youngs_server.model import model_fields
from flask_restful import Resource, Api, reqparse, abort, marshal
from flask import Blueprint, session
from youngs_server.model.UserChannel import UserChannel
from youngs_server.common.decorator import token_required

reload(sys)
sys.setdefaultencoding('utf-8')
apiChannelInfo = Blueprint('channel_info', __name__, url_prefix='/api/channelInfo')
channelInfoRest = Api(apiChannelInfo)


class ChannelList(Resource):
    # 채널 api

    def __init__(self):
        self.channel_post_parser = reqparse.RequestParser()
        self.channel_post_parser.add_argument(
            'type', dest='type',
            location='json', required=True,
            type=str,
            help='channel type d-default, b-best, r-recommand'
        )

    @token_required
    def get(self):
        """ return channel list depending on type"""

        userId = session['userId']
        args = self.channel_post_parser.parse_args()
        channelList = dbManager.__session.query(UserChannel).filter(userId = userId, type=args.type).all()

        return marshal({'results': channelList}, model_fields.channel_list_fields)


channelInfoRest.add_resource(ChannelList, '')
