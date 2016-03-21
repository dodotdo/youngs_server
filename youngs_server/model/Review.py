# -*- coding: utf-8 -*-


from sqlalchemy import Column, Integer, String, Float, Date, ForeignKey, Boolean, Time
from sqlalchemy.orm import relationship
from youngs_server.model import Base
from youngs_server.model import User


class Review(Base):
    __tablename__ = 'review'

    userId = Column(Integer, ForeignKey(User.userId))
    rate = Column(Float, unique=False)
    review = Column(String(500), unique=False)
    uploadDate = Column(Date, unique=False)
    channelId = Column(Integer, unique=False)
    teacherId = Column(Integer, unique=False)

    user = relationship('User', backref='review')

    # id는 자동생성
    def __init__(self, userId, rate, review, uploadDate, channelId, teacherId):
        self.userId= userId
        self.rate = rate
        self.review = review
        self.uploadDate = uploadDate
        self.channelId = channelId
        self.teacherId = teacherId

    def __repr__(self):
        return '<Channel %r>' % self.userId
