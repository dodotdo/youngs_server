# -*- coding: utf-8 -*-


from sqlalchemy import Column, Integer, String, ForeignKey, Boolean, Time, Text
from sqlalchemy.orm import relationship
from youngs_server.model import Base, User


class Channel(Base):
    __tablename__ = 'channel'

    channelId = Column(Integer, primary_key=True, autoincrement=True)
    title = Column(String(30))
    description = Column(Text)
    teacherId = Column(Integer, ForeignKey('user.userId'))
    youtubeURL = Column(String(100))
    isFree = Column(Boolean)
    teachingDay = Column(Integer)
    teachingStartTime = Column(Time)
    teachingEndTime = Column(Time)
    price = Column(Integer)
    listeningLimitCnt = Column(Integer)
    coverImageFileNameOriginal = Column(Text)
    fileName = Column(Text)
    fileSize = Column(Integer)


    user = relationship('User', backref='channel', cascade='save-update, delete')


    def __repr__(self):
        return '<Channel %r %r>' % (self.title, self.description)
