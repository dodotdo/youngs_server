# -*- coding: utf-8 -*-


from sqlalchemy import Column, Integer, String, ForeignKey, Boolean, Time
from sqlalchemy.orm import relationship
from youngs_server.model import Base
from youngs_server.model import User


class Channel(Base):
    __tablename__ = 'channel'

    channelId = Column(Integer, primary_key=True, autoincrement=True)
    title = Column(String(30), unique=False)
    description = Column(String(450), unique=False)
    teacherId = Column(Integer, ForeignKey(User.userId))
    youtubeURL = Column(String(100), unique=False)
    isFree = Column(Boolean, unique=False)
    teachingDay = Column(Integer, unique=False)
    teachingStartTime = Column(Time, unique=False)
    teachingEndTime = Column(Time, unique=False)
    price = Column(Integer, unique=False)
    listeningLimitCnt = Column(Integer, unique=False)
    coverImageFileNameOriginal = Column(String(400), unique=False)
    fileName = Column(String(400), unique=False)
    fileSize = Column(Integer, unique=False)

    userChannel = relationship('UserChannel',
                               backref='channel')
    user = relationship('User', backref='channel')
    review = relationship('Review', backref='channel')

    # id는 자동생성
    def __init__(self, title, description, teacherId, youtubeURL, isFree, teachingDay, teachingStartTime,
                 teachingEndTime, price, listeningLimitCnt, coverImageFileNameOriginal, fileName, fileSize):
        self.title = title
        self.description = description
        self.teacherId = teacherId
        self.youtubeURL = youtubeURL
        self.isFree = isFree
        self.teachingDay = teachingDay
        self.teachingStartTime = teachingStartTime
        self.teachingEndTime = teachingEndTime
        self.price = price
        self.listeningLimitCnt = listeningLimitCnt
        self.coverImageFileNameOriginal = coverImageFileNameOriginal
        self.fileName = fileName
        self.fileSize = fileSize

    def __repr__(self):
        return '<Channel %r %r>' % (self.title, self.description)
