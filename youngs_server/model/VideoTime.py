# -*- coding: utf-8 -*-


from sqlalchemy import Column, Boolean, ForeignKey, Integer, Time
from sqlalchemy.orm import relationship
from youngs_server.model import Base, User, Channel

class VideoTime(Base):
    __tablename__ = 'video'

    teacherId = Column(Integer, ForeignKey=('user.userId'), primary_key=True)
    channelId = Column(Integer, ForeignKey=('channel.channelId'), primary_key=True)
    nowYoutubeTime = Column(Time)
    updatedTime = Column(Time)
    isPlaying = Column(Boolean)

    channel = relationship('Channel', backref='video', cascade='save-update, delete')
    teacher = relationship('User', backref='video', cascade='save-update, delete')

