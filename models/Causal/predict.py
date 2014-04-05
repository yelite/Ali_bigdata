#coding=utf-8

import os
from datetime import timedelta

from sqlalchemy import desc

from .db import s
from models.data import Data
from models.static import StaticData
from models.base import BasePredictor
from .model import Brand, Customer
from .train import INV
from helper import record_aggregate


class Predictor(BasePredictor):
    def __init__(self, ext_session, session=s,
                 static_data=None, test=False):
        super(Predictor, self).__init__(ext_session, static_data, test)

        brands = session.query(Brand).all()
        self.brands = {x.id: x for x in brands}
        customers = session.query(Customer).all()
        self.customers = {x.id: x for x in customers}

        self.all = float(len(self.customers.keys()))

    def predict(self, threshold=1):
        self.begin()
        suggestion = self.calculate_score()

        rv = self.judge_purchase(suggestion, threshold)

        p_count = 0
        for id, brands in rv.items():
            p_count += len(brands)
        print(p_count)

        return rv

    def calculate_score(self):
        return {k.id: self._predict(k) for k in self.customers.values()}

    def _predict(self, c):
        brand_ids = self.user_brand.get(c.id, frozenset())
        if c.idle:
            return self._predict_idle(c, brand_ids)

        brand_score = {k: self._calculate_score(c, self.brands.get(k))
                       for k in brand_ids}

        self.done()
        return brand_score

    def _predict_idle(self, c, brand_ids):
        dt = timedelta(INV)
        brands = []
        score = {}
        for b in brand_ids:
            history = self.data_query.filter(Data.user_id == c.id,
                                             Data.brand_id == b,
                                             Data.time > self.end_date - dt,
                                             Data.time <= self.end_date).all()
            data = record_aggregate(history, unique_brand=True)
            if data[2] or data[3]:
                brands.append(b)
                continue
            score[b] = data[0]
        o_brands = [k for k, v in score.items() if v > 4]
        o_brands = sorted(o_brands, key=score.get, reverse=True)
        o_brands = o_brands[:2]
        brands.extend(o_brands)
        brand_score = {k: 1000 for k in brands}
        return brand_score

    def _calculate_score(self, c, brand):
        dt = timedelta(2 * INV)
        cp = c.click_purchase
        pp = brand.purchase_purchase

        history = self.data_query.filter(Data.user_id == c.id,
                                         Data.brand_id == brand.id,
                                         Data.time > self.end_date - dt,
                                         Data.time <= self.end_date).all()

        data = record_aggregate(history, unique_brand=True)
        if data[3] + data[2] - data[1] > 0:
            return 1000
        return cp * data[0] + 2.8 * pp * data[1] + cp * pp * data[0] * 1.4

    def _judge_purchase(self, user_id, brand_score, threshold):
        customer = self.customers.get(user_id)
        limit = int(customer.purchase * 2 / threshold) + 1
        brands = [k for k, v in brand_score.items() if v > threshold]
        brands = sorted(brands, key=brand_score.get, reverse=True)
        return set(brands[:limit])

    def judge_purchase(self, suggestion, threshold):
        return {k: self._judge_purchase(k, v, threshold=threshold)
                for k, v in suggestion.items()}

    def done(self):
        self.count += 1
        if self.count % 128 == 0:
            print self.count / self.all

