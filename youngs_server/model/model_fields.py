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

channel_list_fields = {
    'results': fields.List(fields.Nested(channel_fields))
}

review_fields = {
    'userId' : fields.Integer,
    'rate' : fields.Float,
    'review' : fields.String,
    'uploadDate' : fields.DateTime,
    'channelId' : fields.Integer
}

review_list_fields = {
    'results' : fields.List(fields.Nested(review_fields))
}

user_channel_fields = {
    'userId' : fields.Integer,
    'channelId' : fields.Integer,
    'type' : fields.String,
    'isListening' : fields.Boolean
}