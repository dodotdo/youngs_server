from flask_restful import Resource, Api, fields, reqparse, abort, marshal_with

user_fields = {
    'userId': fields.Integer(attribute='userid'),
    'email': fields.String,
    'nickname' : fields.String,
    'firstName': fields.String(attribute='first_name'),
    'learnClassCnt' : fields.Integer(attribute='learn_class_cnt'),
    'point' : fields.Integer,
    'teachingClassCnt' : fields.Integer
}

channel_fields = {
    'channelId' : fields.Integer,
    'title' : fields.String,
    'description' : fields.String,
    'teacherId' : fields.Integer,
    'youtubeURL' : fields.String,
    'isFree' : fields.Boolean,
    'teachingDay' : fields.Integer,
    'teachingStartTime' : fields.FormattedString('{teaching_start_time.hour}/{teaching_start_time.minute}'),
    'teachingEndTime' : fields.FormattedString('{teaching_end_time.hour}/{teaching_end_time.minute}'),
    'price' : fields.Integer,
    'listeningLimitCnt' : fields.Integer,
    'coverImageFileNameOriginal' : fields.String,
    'fileName' : fields.String,
    'fileSize' : fields.Integer
}