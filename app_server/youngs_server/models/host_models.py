# -*- coding: utf-8 -*-

from datetime import datetime

from ..database import db
from flask import current_app, session
from itsdangerous import (TimedJSONWebSignatureSerializer
                          as Serializer, BadSignature, SignatureExpired)
from werkzeug.security import generate_password_hash, \
     check_password_hash
from ..common.time_util import datetime_to_rfc822, dump_date, now_datetime, dump_datetime, str_to_datetime
from ..common.values import RequirementStatus

"""
Inheritance
reference : docs.sqlalchemy.org/en/latest/orm/inheritance.html

"""
class Member(db.Model):
    __tablename__ = 'member'
    id = db.Column(db.Integer, primary_key=True, nullable=False)
    email = db.Column(db.String(128), nullable=False, unique=True)
    nickname = db.Column(db.String(64), nullable=False)
    profile_filename = db.Column(db.String(64))
    profile_url = db.Column(db.String(128))
    password_hash = db.Column(db.String(256), nullable=False)
    register_timestamp = db.Column(db.DateTime, default=datetime.utcnow)
    recent_login_timestamp = db.Column(db.DateTime, onupdate=datetime.utcnow)

    lecture_num = db.Column(db.Integer, default=0)
    review_num = db.Column(db.Integer, default=0)
    point_sum = db.Column(db.Integer, default=0)
    point_avg = db.Column(db.Float, default=0)

    lecture_list = db.relationship('Lecture', order_by="desc(Lecture.register_timestamp)", cascade='save-update, delete', lazy="joined")
    review_list = db.relationship('Review', cascade='save-update, delete', lazy="joined")
    attend_list = db.relationship('Attend', order_by="desc(Attend.register_timestamp)", cascade='save-update, delete', lazy="joined")
    voice = db.relationship('Voice', cascade='save-update, delete', lazy='noload')
    review_list = db.relationship('Review', cascade='save-update, delete', lazy="noload")

    def __init__(self, **kwargs):
        super(Member, self).__init__(**kwargs)

    def hash_password(self, password):
        self.password_hash = generate_password_hash(password)

    @property
    def is_authenticated(self):
        if 'user_id' in session and str(session['user_id']) == str(self.id):
            return True
        else:
            return False

    def is_active(self):
        return True

    def is_anonymous(self):
        return False

    def get_id(self):
        return str(self.id)

    def __repr__(self):
        return '<User %r>' % (self.email)

    def verify_password(self, password):
        result = check_password_hash(self.password_hash, password)
        return result

    def generate_auth_token(self, expiration=360000):
        s = Serializer(current_app.config['SECRET_KEY'], expires_in=expiration)
        return s.dumps({'id': self.id})

    def new_point(self, point):
        self.review_num += 1
        self.point_sum += point
        self.point_avg = self.point_sum / self.review_num if point is not None else 0



class Lecture(db.Model):
    __tablename__ = 'lecture'
    id = db.Column(db.Integer, autoincrement=True, primary_key=True, nullable=False)
    title = db.Column(db.String(128), nullable=False)
    description = db.Column(db.Text)
    type = db.Column(db.String(64), nullable=False)
    img_filename = db.Column(db.String(128))
    img_url = db.Column(db.String(128))
    review_num = db.Column(db.Integer, default=0)
    point_sum = db.Column(db.Integer, default=0)
    point_avg = db.Column(db.Float, default=0)

    member_id = db.Column(db.Integer, db.ForeignKey('member.id'))
    is_live = db.Column(db.Boolean, default=False)
    register_timestamp = db.Column(db.DateTime, default=datetime.utcnow)

    member = db.relationship('Member',  uselist=False)
    review_list = db.relationship('Review', order_by="desc(Review.register_timestamp)", cascade='save-update, delete', lazy="joined")
    attend_list = db.relationship('Attend', order_by="desc(Attend.register_timestamp)", cascade='save-update, delete', lazy="joined")
    voice = db.relationship('Voice', cascade='save-update, delete', lazy='noload')

    def new_point(self, point):
        self.review_num += 1
        self.point_sum += point
        self.point_avg = self.point_sum / self.review_num if point is not None else 0


class Review(db.Model):
    __tablename__ = 'review'
    id = db.Column(db.Integer, autoincrement=True, primary_key=True, nullable=False)
    member_id = db.Column(db.Integer, db.ForeignKey('member.id'), nullable=False)
    lecture_id = db.Column(db.Integer, db.ForeignKey('lecture.id'), nullable=False)
    point = db.Column(db.Integer, default=0)
    content = db.Column(db.Text)
    register_timestamp = db.Column(db.DateTime, default=datetime.utcnow)

    member = db.relationship("Member", cascade='save-update')

class Attend(db.Model):
    __tablename__ = 'attend'
    member_id = db.Column(db.Integer, db.ForeignKey('member.id'), primary_key=True)
    lecture_id = db.Column(db.Integer, db.ForeignKey('lecture.id'), primary_key=True)
    register_timestamp = db.Column(db.DateTime, default=datetime.utcnow)


class Question(db.Model):
    __tablename__ = 'question'
    id = db.Column(db.Integer, autoincrement=True, primary_key=True, nullable=False)
    type = db.Column(db.String(64), nullable=False)
    content = db.Column(db.Text)

    voice = db.relationship('Voice', cascade='save-update, delete', lazy='noload')



class Voice(db.Model):
    __tablename__ = 'voice'
    id = db.Column(db.Integer, autoincrement=True, primary_key=True)
    member_id = db.Column(db.Integer, db.ForeignKey('member.id'), primary_key=True)
    lecture_id = db.Column(db.Integer, db.ForeignKey('lecture.id'), nullable=False)
    question_id = db.Column(db.Integer, db.ForeignKey('question.id'), nullable=False)
    voice_filename = db.Column(db.String(128))
    voice_url = db.Column(db.String(128))
    register_timestamp = db.Column(db.DateTime, default=datetime.utcnow)

    member = db.relationship("Member", cascade='save-update')

class Advertize(db.Model):
    __tablename__ = 'advertize'
    id = db.Column(db.Integer, autoincrement=True, primary_key=True)
    img_filename = db.Column(db.String(128))
    img_url = db.Column(db.String(128))
