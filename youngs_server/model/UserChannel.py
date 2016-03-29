# -*- coding: utf-8 -*-


from sqlalchemy import Column, Integer, ForeignKey, Boolean, String
from sqlalchemy.orm import relationship
from youngs_server.model import Base
from youngs_server.model import User
from youngs_server.model import Channel

class UserChannel(Base):
    __tablename__ = 'userChannel'

    num = Column(Integer, autoincrement=True, primary_key=True)
    userId = Column(Integer, ForeignKey(User.userId))
    channelId = Column(Integer, ForeignKey(Channel.channelId))
    #d - default, f-favorite, r-read, fr-favorite&read
    type = Column(String)
    isListening = Column(Boolean)

    user = relationship('User', backref='userChannel', cascade='save-update, delete')
    channel = relationship('Channel', backref='userChannel', cascade='save-update, delete')


    def __repr__(self):
        return '<Channel %r %r>' % (self.userId, self.channelId)