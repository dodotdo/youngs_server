# -*- coding: utf-8 -*-


from sqlalchemy import Column, Integer, ForeignKey, Boolean, String
from sqlalchemy.orm import relationship
from youngs_server.model import Base
from youngs_server.model import User
from youngs_server.model import Channel

class UserChannel(Base):
    __tablename__ = 'userChannel'


    userId = Column(Integer, ForeignKey(User.userId))
    channelId = Column(Integer, ForeignKey(Channel.channelId))
    #d - default, f-favorite, r-read, fr-favorite&read
    type = Column(String, unique=False)
    isListening = Column(Boolean, unique=False)

    user = relationship('User', backref='userChannel', cascade='save-update, delete')
    channel = relationship('Channel', backref='userChannel', cascade='save-update, delete')

    # id는 자동생성
    def __init__(self, userId, channelId, type, isListening):
        self.userId = userId
        self.channelId = channelId
        self.type = type
        self.isListening = isListening

    def __repr__(self):
        return '<Channel %r %r>' % (self.userId, self.channelId)