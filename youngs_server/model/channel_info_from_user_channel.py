# -*- coding: utf-8 -*-


from sqlalchemy import Column, Integer, Float, Boolean
from youngs_server.database import db


class ChannelInfoModel(db.Model):
    __tablename__ = 'channelinfo'

    channelId = Column(Integer, primary_key=True)
    nowCnt = Column(Integer)
    favoriteCnt = Column(Integer)
    readCnt = Column(Integer)
    isFavorite = Column(Boolean)
    isRead = Column(Boolean)
    classCnt = Column(Integer)  #by teacher
    rate = Column(Float)
    reviewCnt = Column(Integer)
