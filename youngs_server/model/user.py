# -*- coding: utf-8 -*-


from sqlalchemy import Column, Integer, String
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
    password = Column(String(55), unique=False)
    nickname = Column(String(15), unique=True)
    imageFileNameOriginal = Column(String(400), unique=False)
    fileName = Column(String(400), unique=False)
    fileSize = Column(Integer, unique=False)
    learnClassCnt = Column(Integer, unique=False)
    point = Column(Integer, unique=False)
    teachingClassCnt = Column(Integer, unique=False)

    # id는 자동생성
    def __init__(self, email, password, nickname, imageFileNameOriginal, fileName, fileSize, learnClassCnt, point,
                 teachingClassCnt):
        self.email = email
        self.password = password
        self.nickname = nickname
        self.imageFileNameOriginal = imageFileNameOriginal
        self.fileName = fileName
        self.fileSize = fileSize
        self.learnClassCnt = learnClassCnt
        self.point = point
        self.teachingClassCnt = teachingClassCnt

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
