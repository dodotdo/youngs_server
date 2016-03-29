# -*- coding: utf-8 -*-


from sqlalchemy import Column, Integer, Float, Date, ForeignKey, Text
from sqlalchemy.orm import relationship
from youngs_server.model import Base
from youngs_server.model import User, Channel


class Review(Base):
    __tablename__ = 'review'

    userId = Column(Integer, ForeignKey(User.userId))
    rate = Column(Float)
    review = Column(Text)
    uploadDate = Column(Date)
    channelId = Column(Integer, ForeignKey(Channel.channelId), primary_key=True)

    user = relationship('User', backref='review', cascade='save-update, delete')
    channel = relationship('Channel', backref='review', cascade='save-update, delete')


    def __repr__(self):
        return '<Channel %r>' % self.userId
