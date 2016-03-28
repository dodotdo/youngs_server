# -*- coding: utf-8 -*-


from sqlalchemy import Column, Boolean, ForeignKey, Integer
from sqlalchemy.orm import relationship
from youngs_server.model import Base, User, Channel
import time

class VideoTime(Base):
    __tablename__ = 'video'

    teacherId = Column(Integer, ForeignKey=(User.userId))
    channelId = Column(Integer, ForeignKey=(Channel.channelId))
    nowYoutubeTime = Column(time, unique=False)
    updatedTime = Column(time, unique=False)
    isPlaying = Column(Boolean, unique=False)

    channel = relationship('Channel', backref='video', cascade='save-update, delete')
    teacher = relationship('User', backref='video', cascade='save-update, delete')

    def __init__(self, channelId, nowYoutubeTime, updatedTime, isPlaying):
        self.channelId = channelId
        self.nowYoutubeTime = nowYoutubeTime
        self.updatedTime = updatedTime
        self.isPlaying = isPlaying

