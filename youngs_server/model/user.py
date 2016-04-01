# -*- coding: utf-8 -*-


from sqlalchemy import Column, Integer, String, Text
from youngs_server.youngs_logger import Log
from youngs_server.database import db
from werkzeug.security import generate_password_hash, check_password_hash
from flask import current_app
from itsdangerous import (TimedJSONWebSignatureSerializer
                          as Serializer, BadSignature, SignatureExpired)


class User(db.Model):
    __tablename__ = 'user'

    userId = Column(Integer, primary_key=True, autoincrement=True)
    email = Column(String(50), unique=True)
    hashedPassword = Column(String(55))
    nickname = Column(String(15), unique=True)
    imageFileNameOriginal = Column(Text)
    fileName = Column(Text)
    fileSize = Column(Integer)
    learnClassCnt = Column(Integer)
    point = Column(Integer)
    teachingClassCnt = Column(Integer)


    def __repr__(self):
        return '<User %r %r>' % (self.nickname, self.email)

    def hash_password(self, password):
        self.hashedPassword = generate_password_hash(password)

    def verify_password(self, password):
        return check_password_hash(self.hashedPassword, password)

    def generate_auth_token(self, expiration=360000):
        s = Serializer(current_app.config['SECRET_KEY'], expires_in=expiration)

        return s.dumps({'userId': self.userId})

    @staticmethod
    def verify_auth_token(token):
        s = Serializer(current_app.config['SECRET_KEY'])
        try:
            data = s.loads(token)
        except SignatureExpired:
            return None    # valid token, but expired
        except BadSignature:
            return None    # invalid token
        user = User.query.get(data['userId'])
        return user
