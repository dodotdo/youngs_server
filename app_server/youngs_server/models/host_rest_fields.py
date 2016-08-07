from ..customlib.flask_restful import Resource, Api, fields, reqparse, abort, marshal_with
from ..common.values import RequirementStatus

auth_member_fields = {
    'token': fields.String,
    'id': fields.Integer,
    'email': fields.String,
    'nickname': fields.String,
    'profile_url': fields.String,
    'recent_login_timestamp': fields.DateTime,
    'register_timestamp': fields.DateTime
}
member_fields = {
    'normal': {
        'id': fields.Integer,
        'email': fields.String,
        'nickname': fields.String,
        'point_avg': fields.Float,
        'review_num': fields.Integer,
        'lecture_num': fields.Integer,
        'profile_url': fields.String,
        'recent_login_timestamp': fields.DateTime,
        'register_timestamp': fields.DateTime
    },
    'lecture': {
        'id': fields.Integer,
        'email': fields.String,
        'nickname': fields.String,
        'point_avg': fields.Float,
        'review_num': fields.Integer,
        'lecture_num': fields.Integer,
        'profile_url': fields.String,
        'recent_login_timestamp': fields.DateTime,
        'register_timestamp': fields.DateTime
        # lecture list
    },
    'attend': {
        'id': fields.Integer,
        'email': fields.String,
        'nickname': fields.String,
        'point_avg': fields.Float,
        'review_num': fields.Integer,
        'lecture_num': fields.Integer,
        'profile_url': fields.String,
        'recent_login_timestamp': fields.DateTime,
        'register_timestamp': fields.DateTime
        # attend list
    }
}


member_list_fields = {
    'normal': {
        'results': fields.List(fields.Nested(member_fields['normal'], allow_null=True))
    },
    'lecture': {
        'results': fields.List(fields.Nested(member_fields['lecture'], allow_null=True))
    },
    'attend': {
        'results': fields.List(fields.Nested(member_fields['attend'], allow_null=True))
    }
}


review_fields = {
    'normal': {
        'id': fields.Integer,
        'member': fields.Nested(member_fields['normal']),
        'point': fields.Integer,
        'content': fields.String,
        'register_timestamp': fields.DateTime
    }
}

review_list_fields = {
    'normal': {
        'results': fields.List(fields.Nested(review_fields['normal']))
    }

}


lecture_fields = {
    'normal': {
        'id': fields.Integer,
        'title': fields.String,
        'description': fields.String,
        'type': fields.String,
        'img_url': fields.String,
        'point_avg': fields.Float,
        'status': fields.String,
        'member': fields.Nested(member_fields['normal']),
        'register_timestamp': fields.DateTime
    },
    'review': {
        'id': fields.Integer,
        'title': fields.String,
        'description': fields.String,
        'type': fields.String,
        'point_avg': fields.Float,
        'status': fields.String,
        'img_url': fields.String,
        'member': fields.Nested(member_fields['normal']),
        'register_timestamp': fields.DateTime,
        'review_list': fields.List(fields.Nested(review_fields['normal'], allow_null=True))
    },
    'listener': {
        'id': fields.Integer,
        'title': fields.String,
        'description': fields.String,
        'type': fields.String,
        'point_avg': fields.Float,
        'status': fields.String,
        'img_url': fields.String,
        'member': fields.Nested(member_fields['normal']),
        'register_timestamp': fields.DateTime,
        'listener': fields.Nested(member_fields['normal'], allow_null=True)
    },
    'full': {
        'id': fields.Integer,
        'title': fields.String,
        'description': fields.String,
        'type': fields.String,
        'point_avg': fields.Float,
        'status': fields.String,
        'img_url': fields.String,
        'member': fields.Nested(member_fields['normal']),
        'register_timestamp': fields.DateTime,
        'listener': fields.Nested(member_fields['normal'], allow_null=True),
        'review_list': fields.List(fields.Nested(review_fields['normal'], allow_null=True))
    }
}



lecture_list_fields = {
    'normal': {
        'results': fields.List(fields.Nested(lecture_fields['normal'], allow_null=True))
    },
    'review': {
        'results': fields.List(fields.Nested(lecture_fields['review'], allow_null=True))
    },
    'listener': {
        'results': fields.List(fields.Nested(lecture_fields['listener'], allow_null=True))
    }
}

question_fields = {
    'id': fields.Integer,
    'type': fields.String,
    'content': fields.String
}

question_list_fields = {
    'results': fields.List(fields.Nested(question_fields, allow_null=False))
}


voice_fields = {
    'id': fields.Integer,
    'member': fields.Nested(member_fields['normal']),
    'voice_url': fields.String,
    'register_timestamp': fields.DateTime

}

voice_list_fields = {
    'results': fields.List(fields.Nested(voice_fields, allow_null=False))
}