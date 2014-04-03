#coding=utf-8

import os
from datetime import timedelta

from sqlalchemy import desc

from .db import s
from models.data import Data
from models.static import StaticData
from .model import Brand, Customer
from .train import INV
from helper import record_aggregate


class Predictor:
    def __init__(self, ext_session, session=s, test=False):
        self.ext_session = ext_session
        self.end_date = ext_session.query(Data.time).order_by(desc(Data.time)).first()[0]
        self.test = test

        brands = session.query(Brand).all()
        self.brands = {x.id: x for x in brands}
        customers = session.query(Customer).all()
        self.customers = {x.id: x for x in customers}
        self.data_query = self.ext_session.query(Data)

        self.count = 0
        self.all = float(len(self.customers.keys()))

        self.static_data = StaticData(test=test)
        self.user_brand = self.static_data.user_brand

    def predict(self, threshold=1):
        user_score = self.calculate_user_brand_score()
        return [(k.id, self._judge_purchase(k, v, threshold=threshold))
                for k, v in user_score]

    def calculate_user_brand_score(self):
        self.count = 0
        return map(self._predict, self.customers.values())

    def _predict(self, c):
        brand_ids = self.user_brand.get(c.id, frozenset())
        if c.idle:
            return self._predict_idle(c, brand_ids)

        brand_score = {k: self._calculate_score(c, self.brands.get(k))
                       for k in brand_ids}

        self.done()
        return c, brand_score

    def _predict_idle(self, c, brand_ids):
        dt = timedelta(INV)
        brands = []
        score = {}
        for b in brand_ids:
            history = self.data_query.filter(Data.user_id==c.id,
                                             Data.brand_id==b,
                                             Data.time > self.end_date - dt,
                                             Data.time <= self.end_date).all()
            data = record_aggregate(history, unique_brand=True)
            if data[2] or data[3]:
                brands.append(b)
                continue
            score[b] = data[0]
        o_brands = [k for k,v in score.items() if v > 4]
        o_brands = sorted(o_brands, key=score.get, reverse=True)
        o_brands = o_brands[:2]
        brands.extend(o_brands)
        brand_score = {k:1000 for k in brands}
        return c, brand_score

    def _calculate_score(self, c, brand):
        dt = timedelta(2*INV)
        cp = c.click_purchase
        pp = brand.purchase_purchase

        history = self.data_query.filter(Data.user_id==c.id,
                                         Data.brand_id==brand.id,
                                         Data.time > self.end_date - dt,
                                         Data.time <= self.end_date).all()

        data = record_aggregate(history, unique_brand=True)
        if data[3]+data[2]-data[1]>0:
            return 1000
        return cp*data[0] + 2*pp*data[1] + cp*pp*data[0]

    @staticmethod
    def _judge_purchase(customer, brand_score, threshold):
        limit = int(customer.purchase)*5+1
        brands = [k for k,v in brand_score.items() if v > threshold]
        brands = sorted(brands, key=brand_score.get, reverse=True)
        return brands[:limit]

    def done(self):
        self.count += 1
        if self.count % 128 == 0:
            print self.count / self.all

