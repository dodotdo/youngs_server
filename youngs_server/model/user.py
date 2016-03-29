# -*- coding: utf-8 -*-


from sqlalchemy import Column, Integer, String, Text
from sqlalchemy.orm import relationship
from youngs_server.model import Base
from werkzeug.security import generate_password_hash, check_password_hash
from flask import current_app
from itsdangerous import (TimedJSONWebSignatureSerializer
                          as Serializer, BadSignature, SignatureExpired)


class User(Base):
    __tablename__ = 'user'

    userId = Column(Integer, primary_key=True, autoincrement=True)
    email = Column(String(50), unique=True)
    password = Column(String(55))
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
        self.password = generate_password_hash(password)

    def verify_password(self, password):
        return check_password_hash(self.password_hash, password)

    def generate_auth_token(self, expiration=360000):
        s = Serializer(current_app.config['SECRET_KEY'], expires_in=expiration)
        print 'origin token', s.dumps({'id': self.id})

        return s.dumps({'id': self.id})
