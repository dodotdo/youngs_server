# -*- coding: utf-8 -*-

import sys
from youngs_server.database import dbManager
from youngs_server.model import model_fields
from youngs_server.common.Util import timeToString
from flask_restful import Resource, Api, reqparse, abort, marshal
from flask import Blueprint, request, session, current_app
from youngs_server.model.Channel import Channel
from youngs_server.common.decorator import token_required
from pil import Image
from werkzeug.utils import secure_filename
from youngs_server.youngs_logger import Log
import uuid, os

reload(sys)
sys.setdefaultencoding('utf-8')
apiMakeChannel = Blueprint('channel', __name__, url_prefix='/api/makeChannel')
makeChannelRest = Api(apiMakeChannel)

ALLOWED_EXTENSIONS = set(['jpg', 'jpeg', 'png'])


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

    @token_required
    def post(self):
        """makeChannel"""
        args = self.make_channel_post_parser.parse_args()

        """중복 채널 처리"""
        duplicateChannel = Channel.query.filter_by(title=args.title).first()

        if duplicateChannel is not None:
            return abort(401, message='duplicate channel title')

        """사진 처리"""
        if args.coverImageFileNameOriginal is None:
            coverImage = ''
        else:
            coverImage = args.coverImageFileNameOriginal

        filename = None
        filesize = 0
        filename_orig = coverImage.filename

        try:
            #: 파일 확장자 검사 : 현재 jpg, jpeg, png만 가능
            if coverImage and ('.' in coverImage and coverImage.rsplit('.', 1)[1].lower() in ALLOWED_EXTENSIONS):

                ext = (coverImage.filename).rsplit('.', 1)[1]

                #: 업로드 폴더 위치는 얻는다.
                upload_folder = \
                    os.path.join(current_app.root_path,
                                 current_app.config['UPLOAD_CHANNEL_COVER_FOLDER'])
                #: 유일하고 안전한 파일명을 얻는다.
                filename = \
                    secure_filename(args.teacherId +
                                    '_' +
                                    unicode(uuid.uuid4()) +
                                    "." +
                                    ext)

                coverImage.save(os.path.join(upload_folder,
                                             filename))

                filesize = os.stat(upload_folder + filename).st_size

            else:
                raise Exception("File upload error : illegal file.")

        except Exception as e:
            Log.error(str(e))
            raise e

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
            coverImageFileNameOriginal=filename_orig,
            fileName=filename,
            fileSize=filesize
        )

        dbManager.__session.add(channel)
        dbManager.__session.commit()

        return marshal(channel, model_fields.channel_fields, envelope='results')


makeChannelRest.add_resource(MakeChannel, '')


def __allowed_file(filename):
    return
