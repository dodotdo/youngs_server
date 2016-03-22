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
