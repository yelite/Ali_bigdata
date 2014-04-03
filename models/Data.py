#coding=utf-8


import os

from sqlalchemy import Column, Integer, Date
from sqlalchemy.ext.declarative import declarative_base

from helper import root_dic


Base = declarative_base()


class Data(Base):
    __tablename__ = 'data'

    id = Column(Integer, primary_key=True)
    user_id = Column(Integer, index=True, nullable=False)
    brand_id = Column(Integer, index=True, nullable=False)
    time = Column(Date, index=True, nullable=False)
    action = Column(Integer, nullable=False)
