# -*- coding: utf-8 -*-


from sqlalchemy import Column, Boolean, ForeignKey, Integer, DateTime
from sqlalchemy.orm import relationship
from youngs_server.database import db

class VideoTime(db.Model):
    __tablename__ = 'video'

    teacherId = Column(Integer, ForeignKey('user.userId'), primary_key=True)
    channelId = Column(Integer, ForeignKey('channel.channelId'), primary_key=True)
    nowYoutubeTimeHour = Column(Integer)
    nowYoutubeTimeMinute = Column(Integer)
    nowYoutubeTimeSecond = Column(Integer)
    updatedTime = Column(DateTime)
    isPlaying = Column(Boolean)

    channel = relationship('Channel', backref='video', cascade='save-update, delete')
    teacher = relationship('User', backref='video', cascade='save-update, delete')

