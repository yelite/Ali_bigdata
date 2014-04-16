#coding=utf-8

from sqlalchemy import Column, Integer, Date
from sqlalchemy.ext.declarative import declarative_base
import os


Base = declarative_base()

root_dic = os.path.split(os.path.realpath(__file__))[0]
root_dic = os.path.join(root_dic, '..')

class Data(Base):
    __tablename__ = 'data'

    id = Column(Integer, primary_key=True)
    user_id = Column(Integer, index=True, nullable=False)
    brand_id = Column(Integer, index=True, nullable=False)
    time = Column(Date, index=True, nullable=False)
    action = Column(Integer, nullable=False)

class StaticData:
    def __init__(self, test=False):
        data_dir = 'tests/data' if test else 'data'
        name = 'user_brand.txt'
        path = os.path.join(root_dic,
                            data_dir,
                            name)
        self.user_brand = self.init_user_brand(path)

        name = 'brand_user.txt'
        path = os.path.join(root_dic,
                            data_dir,
                            name)
        self.brand_user = self.init_brand_user(path)

    @staticmethod
    def init_user_brand(path):
        f = open(path)
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

    @staticmethod
    def init_brand_user(path):
        f = open(path)
        rv = {}
        count = 0
        for l in f:
            name, users = l.split('\t')
            users = users.strip()
            if not users:
                rv[int(name)] = set()
                continue
            users = map(int, users.split(','))
            count += len(users)
            rv[int(name)] = set(users)
        f.close()
        return rv