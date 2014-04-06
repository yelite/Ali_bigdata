#coding=utf-8


from sqlalchemy import desc

from data import Data
from static import StaticData


class BasePredictor(object):
    def __init__(self, ext_session, static_data=None, test=False):
        self.ext_session = ext_session
        self.test = test

        self.data_query = self.ext_session.query(Data)

        self.end_date = ext_session.query(Data.time).order_by(desc(Data.time)).first()[0]
        self.start_date = ext_session.query(Data.time).order_by(Data.time).first()[0]
        self.length = (self.end_date - self.start_date).days

        self.count = 0
        self.all = 0

        if static_data:
            self.static_data = static_data
        else:
            self.static_data = StaticData(test=test)
        self.user_brand = self.static_data.user_brand
        self.brand_user = self.static_data.brand_user

    def begin(self):
        self.count = 0

    def done(self):
        self.count += 1
        if self.count % 128 == 0:
            print self.count / self.all