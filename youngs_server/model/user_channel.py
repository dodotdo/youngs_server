# -*- coding: utf-8 -*-


from sqlalchemy import Column, Integer, ForeignKey, Boolean, String
from sqlalchemy.orm import relationship
from youngs_server.database import db

class UserChannel(db.Model):
    __tablename__ = 'userChannel'

    num = Column(Integer, autoincrement=True, primary_key=True)
    userId = Column(Integer, ForeignKey('user.userId'))
    channelId = Column(Integer, ForeignKey('channel.channelId'))
    #d - default, f-favorite, r-read, fr-favorite&read
    type = Column(String)
    isListening = Column(Boolean)

    user = relationship('User', backref='userChannel', cascade='save-update, delete')
    channel = relationship('Channel', backref='userChannel', cascade='save-update, delete')


    def __repr__(self):
        return '<Channel %r %r>' % (self.userId, self.channelId)