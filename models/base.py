#coding=utf-8


from sqlalchemy import Column, Integer, Float, Date
from sqlalchemy.ext.declarative import declarative_base
from helper import root_dic
from db import Session
import os


Base = declarative_base()


class Data(Base):
    __tablename__ = 'data'

    id = Column(Integer, primary_key=True)
    user_id = Column(Integer, index=True, nullable=False)
    brand_id = Column(Integer, index=True, nullable=False)
    time = Column(Date, index=True, nullable=False)
    action = Column(Integer, nullable=False)

    __mapper_args__ = {'order_by': id.desc()}


class StaticData:
    def __init__(self, test=False):
        name = 'data/user_brand{}.txt'.format('_test' if test else '')
        self.user_brand_file = os.path.join(root_dic, name)
        self.user_brand = self.init_user_brand()

    def init_user_brand(self):
        f = open(self.user_brand_file)
        rv = {}
        count = 0
        for l in f:
            name, brands = l.split('\t')
            brands = brands.strip()
            if not brands:
                rv[int(name)] = set()
                continue
            brands = map(int, brands.split(','))
            count += len(brands)
            rv[int(name)] = set(brands)
        f.close()
        return rv

static_data = StaticData()