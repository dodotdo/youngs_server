# -*- coding: utf-8 -*-


from sqlalchemy import Column, Integer, ForeignKey
from sqlalchemy.orm import relationship
from youngs_server.model import Base
from youngs_server.model import User
from youngs_server.model import Channel


class UserChannel(Base):
    __tablename__ = 'userChannel'


    userId = Column(Integer, ForeignKey(User.userId))
    channelId = Column(Integer, ForeignKey(Channel.channelId))

    user = relationship('User', backref='userChannel')
    channel = relationship('Channel', backref='userChannel')

    # id는 자동생성
    def __init__(self, userId, channelId):
        self.userId = userId
        self.channelId = channelId

    def __repr__(self):
        return '<Channel %r %r>' % (self.userId, self.channelId)
