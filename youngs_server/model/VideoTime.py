# -*- coding: utf-8 -*-


from sqlalchemy import Column, Boolean, ForeignKey, Integer, Time
from sqlalchemy.orm import relationship
from youngs_server.model import Base, User, Channel

class VideoTime(Base):
    __tablename__ = 'video'

    teacherId = Column(Integer, ForeignKey=(User.userId))
    channelId = Column(Integer, ForeignKey=(Channel.channelId))
    nowYoutubeTime = Column(Time, unique=False)
    updatedTime = Column(Time, unique=False)
    isPlaying = Column(Boolean, unique=False)

    channel = relationship('Channel', backref='video', cascade='save-update, delete')
    teacher = relationship('User', backref='video', cascade='save-update, delete')

    def __init__(self, channelId, nowYoutubeTime, updatedTime, isPlaying):
        self.channelId = channelId
        self.nowYoutubeTime = nowYoutubeTime
        self.updatedTime = updatedTime
        self.isPlaying = isPlaying

