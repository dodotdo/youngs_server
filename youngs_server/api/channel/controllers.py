# -*- coding: utf-8 -*-

import sys
import os
import io
import uuid
import binascii
import json
import base64
from youngs_server.database import db
from youngs_server.model import model_fields
from flask_restful import Resource, Api, reqparse, abort, marshal
from flask import Blueprint, session, request, jsonify, current_app
from youngs_server.model.channel import Channel
from youngs_server.model.user_channel import UserChannel
from youngs_server.model.user import User
from youngs_server.common.decorator import token_required
from youngs_server.api.listen.controllers import Listen
from youngs_server.api.review.controllers import ReviewInfo
from youngs_server.api.video.controllers import VideoTimeInfo
from youngs_server.youngs_logger import Log
from werkzeug.utils import secure_filename

reload(sys)
sys.setdefaultencoding('utf-8')
apiChannel = Blueprint('channel', __name__, url_prefix='/api/channels')
channelRest = Api(apiChannel)

ALLOWED_EXTENSIONS = set(['jpg', 'jpeg', 'png'])


class Channels(Resource):
    # 채널 api

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
            'youtubeURL', dest='youtubeURL',
            location='json',
            type=str,
            help='teacher of the channel'
        )
        self.make_channel_post_parser.add_argument(
            'isFree', dest='isFree',
            location='json', required=True,
            type=bool,
            help='channel is free or not'
        )
        self.make_channel_post_parser.add_argument(
            'teachingDay', dest='teachingDay',
            location='json', required=True,
            type=int,
            help='teachingDay of Channel, on-1, off-0'
        )
        self.make_channel_post_parser.add_argument(
            'teachingTime', dest='teachingTime',
            location='json', required=True,
            type=str,
            help='teachingStartTime of Channel'
        )
        self.make_channel_post_parser.add_argument(
            'price', dest='price',
            location='json', required=True,
            type=int,
            help='price of Channel free channel`s price is 0'
        )
        self.make_channel_post_parser.add_argument(
            'favoriteCnt', dest='favoriteCnt',
            location='json', required=True,
            type=int,
            help='favorite cnt of Channel free channel`s price is 0'
        )
        self.make_channel_post_parser.add_argument(
            'readCnt', dest='readCnt',
            location='json', required=True,
            type=int,
            help='read cnt of Channel free channel`s price is 0'
        )
        self.make_channel_post_parser.add_argument(
            'listeningLimitCnt', dest='listeningLimitCnt',
            location='json', required=True,
            type=int,
            help='limit count of person who listen Channel'
        )

    @token_required
    def get(self):
        """ return channel list depending on type"""

        userId = session['userId']
        type = request.args.get('type')
        channelList = db.session.query(UserChannel).filter_by(userId=userId, type=type).all()

        if channelList == []:
            return jsonify({'message': 'channel is not exist'})

        return marshal(channelList, model_fields.channel_list_fields, envelope='results')


    @token_required
    def post(self):
        """makeChannel"""
        args = self.make_channel_post_parser.parse_args()

        """중복 채널 처리"""
        duplicateChannel = db.session.query(Channel).filter_by(title=args.title).first()

        if duplicateChannel is not None:
            return abort(401, message='duplicate channel title')

        teacher = db.session.query(User).filter_by(userId=session['userId']).first()

        channel = Channel(
            title=args.title,
            description=args.description,
            teacherId=session['userId'],
            teacherName=teacher.nickname,
            youtubeURL=args.youtubeURL,
            isFree=args.isFree,
            teachingDay=args.teachingDay,
            teachingTime=args.teachingTime,
            price=args.price,
            listeningLimitCnt=args.listeningLimitCnt,
            coverImageFileNameOriginal="",
            fileName="",
            fileSize=0
        )

        db.session.add(channel)
        db.session.commit()

        return marshal(channel, model_fields.channel_fields, envelope='results')


class ChannelInfo(Resource):
    def get(self, channel_id):
        """ return channel information"""

        channel = db.session.query(Channel).filter_by(channelId=channel_id).first()

        if channel is None:
            return abort(401, message='channelId is not valid')

        return marshal(channel, model_fields.channel_fields, envelope='results')


class ChannelStatus(Resource):
    @token_required
    def put(self, channel_id, type):
        """channel status change"""

        userId = session['userId']
        args = self.channel_status_post_parser.parse_args()
        userChannelModel = UserChannel(
            userId=userId,
            channelId=channel_id,
            type=args.type,
            isListening=False
        )

        nowListeningChannel = db.session.query(UserChannel).filter_by(userId=userId, channelId=channel_id).first()
        channel = db.session.query(Channel).filter_by(channelId=channel_id).first()

        if nowListeningChannel is None:
            """디비에 없는 경우"""

            # 관계는 형성되지 않았지만 채널은 존재하는 경우 관계추가
            if channel is not None:
                db.session.add(userChannelModel)
            else:
                return jsonify({'result': 'doesn`t exist channel'})
        else:
            """디비에 있는 경우"""

            if type == "d":
                pass
            elif type == "r":
                channel.readCnt += 1
            elif type == "f":
                channel.favoriteCnt += 1
            else:
                channel.readCnt += 1
                channel.favoriteCnt += 1

            # type 바뀌기전
            if nowListeningChannel.type == "d":
                pass
            elif nowListeningChannel.type == "r":
                channel.readCnt -= 1
            elif nowListeningChannel.type == "f":
                channel.favoriteCnt -= 1
            else:
                channel.readCnt -= 1
                channel.favoriteCnt -= 1

                nowListeningChannel.type = type

        db.session.commit()

        return marshal(userChannelModel, model_fields.user_channel_fields, envelope='results')

class ChannelPhoto(Resource):
    @token_required
    def put(self, title):
        """ return channel list depending on type"""
        userId = session['userId']
        file = request.form['file'].decode('utf-8')
        file = request.form['file'].encode('utf-8', 'replace').decode('utf-8')
        print request.headers
        # print file2
        #
        # print(file)
        filename = secure_filename(title)+".jpg"
        filepath = os.path.join(current_app.config['UPLOAD_CHANNEL_COVER_FOLDER'], filename)
        if not os.path.exists(filepath):
            with open(filepath, "w+") as f:
                    f.write(file)

        filename = os.path.split(filepath)

        channel = db.session.query(Channel).filter_by(title=title).first()

        if channel is None:
            return abort(202, message="invalid channel")

        channel.coverImageFileNameOriginal = filename

        return marshal(channel, model_fields.channel_fields, envelope='results')


    """
    try:
    #: 파일 확장자 검사 : 현재 jpg, jpeg만 가능
    if file and '.' in filename_orig and filename_orig.rsplit('.', 1)[1].lower() in ALLOWED_EXTENSIONS:

        ext = (filename_orig).rsplit('.', 1)[1]

        #: 업로드 폴더 위치는 얻는다.
        upload_folder = \
            os.path.join(current_app.root_path,
                         current_app.config['UPLOAD_CHANNEL_COVER_FOLDER'])

        #: 유일하고 안전한 파일명을 얻는다.
        filename = \
            secure_filename(title +
                            '_' +
                            unicode(uuid.uuid4()) +
                            "." +
                            ext)

        file.save(os.path.join(upload_folder,
                               filename))

        channel.coverImageFileNameOriginal = filename

        filesize = \
            os.stat(upload_folder + filename).st_size


    else:
        raise Exception("File upload error : illegal file.")

except Exception as e:
    Log.error(str(e))
    raise e
"""




channelRest.add_resource(Channels, '')
channelRest.add_resource(ChannelInfo, '/<channel_id>')
channelRest.add_resource(ChannelStatus, '/<channel_id>/status/<type>')
channelRest.add_resource(Listen, '/<channel_id>/listenstatus')
channelRest.add_resource(ReviewInfo, '/<channel_id>/review')
channelRest.add_resource(VideoTimeInfo, '/<channel_id>/videotime')
channelRest.add_resource(ChannelPhoto, '/photo/<title>')
