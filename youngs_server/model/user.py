# -*- coding: utf-8 -*-


from sqlalchemy import Column, Integer, String, TEXT
from sqlalchemy.orm import relationship
from youngs_server.model import Base


class User(Base):
    __tablename__ = 'user'

    userId = Column(Integer, primary_key=True, autoincrement=True)
    email = Column(String(50), unique=True)
    password = Column(String(55), unique=False)
    nickname = Column(String(15), unique=True)
    imageFileNameOriginal = Column(String(400), unique=False)
    Filename = Column(String(400), unique=False)
    Filesize = Column(Integer, unique=False)
    learnClassCnt = Column(Integer, unique=False)
    point = Column(Integer, unique=False)
    teachingClassCnt = Column(Integer, unique=False)

    userChannel = relationship('UserChannel',
                          backref='user')
    channel = relationship('Channel', backref='user')
    review = relationship('Review', backref='user')

    #id는 자동생성
    def __init__(self, name, email, password):
        self.username = name
        self.email = email
        self.password = password

    def __repr__(self):
        return '<User %r %r>' % (self.username, self.email)