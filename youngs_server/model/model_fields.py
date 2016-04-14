from flask_restful import Resource, Api, fields, reqparse, abort, marshal_with

user_fields = {
    'userId': fields.Integer,
    'token': fields.String,
    'email': fields.String,
    'nickname': fields.String,
    'learnClassCnt': fields.Integer,
    'point': fields.Integer,
    'teachingClassCnt': fields.Integer,
    'password': fields.String
}

channel_fields = {
    'channelId': fields.Integer,
    'title': fields.String,
    'description': fields.String,
    'teacherId': fields.Integer,
    'teacherName': fields.String,
    'youtubeURL': fields.String,
    'isFree': fields.Boolean,
    'favoriteCnt': fields.Integer,
    'readCnt': fields.Integer,
    'teachingDay': fields.Integer,
    'teachingTime': fields.String,
    'price': fields.Integer,
    'listeningLimitCnt': fields.Integer,
    'file': fields.String,
    'fileName': fields.String,
    'fileSize': fields.Integer
}

video_time_fields = {
    'teacherId': fields.Integer,
    'channelId': fields.Integer,
    'playtime': fields.Integer,
    'isPlaying': fields.Boolean
}

channel_list_fields = {
        'results': fields.List(fields.Nested(channel_fields))
}

review_fields = {
    'reviewId': fields.Integer,
    'userId': fields.Integer,
    'rate': fields.Float,
    'review': fields.String,
    'uploadDate': fields.String,
    'channelId': fields.Integer
}

review_list_fields = {
    'results': fields.List(fields.Nested(review_fields))
}

user_channel_fields = {
    'channelId': fields.Integer,
    'nowCnt' : fields.Integer,
    'favoriteCnt' : fields.Integer,
    'readCnt' : fields.Integer,
    'isFavorite' : fields.Boolean,
    'isRead' : fields.Boolean,
    'classCnt' : fields.Integer,
    'rate' : fields.Float,
    'reviewCnt' : fields.Integer
}
