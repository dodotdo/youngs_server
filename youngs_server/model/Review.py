# -*- coding: utf-8 -*-


from sqlalchemy import Column, Integer, Float, Date, ForeignKey, Text, String
from sqlalchemy.orm import relationship
from youngs_server.database import db


class Review(db.Model):
    __tablename__ = 'review'

    reviewId = Column(Integer, primary_key=True)
    userId = Column(Integer, ForeignKey('user.userId'))
    rate = Column(Float)
    review = Column(Text)
    uploadDate = Column(String)
    channelId = Column(Integer, ForeignKey('channel.channelId'))

    user = relationship('User', backref='review', cascade='save-update, delete')
    channel = relationship('Channel', backref='review', cascade='save-update, delete')


    def __repr__(self):
        return '<Channel %r>' % self.userId
