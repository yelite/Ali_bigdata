#coding=utf-8

import os
from datetime import timedelta

from sqlalchemy import desc

from .db import s
from models.data import Data
from models.static import StaticData
from models.base import BasePredictor
from .model import Brand, Customer
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

        self.static_data = StaticData(test=test)
        self.user_brand = self.static_data.user_brand
        self.brand_user = self.static_data.brand_user

    def predict(self, threshold=14):
        self.count = 0
        suggestion = self.calculate_score()

        rv = {k: {l for l, s in v.items() if s > threshold}
              for k, v in suggestion.items()}
        p_count = 0
        for id, brands in rv.items():
            p_count += len(brands)
        print(p_count)
        return rv

    def calculate_score(self):
        return {k: self._calculate_score(k) for k in self.customers.keys()}

    def _calculate_score(self, user_id):
        brand_score = dict()
        brands = self.user_brand.get(user_id, frozenset())
        if not brands:
            return brand_score
        brand_score = {b: self._score(user_id, b) for b in brands}

        self.done()
        return brand_score

    def _score(self, user, brand):
        history = self.data_query.filter(Data.user_id == user,
                                         Data.brand_id == brand).all()

        score = 0
        score_table = {0: 0.1,
                       1: 0.7,
                       2: 1,
                       3: 1}

        all = record_aggregate(history, unique_date=True)
        if all[3] > 1:
            score_table[3] = 3

        for record in history:
            base_score = score_table[record.action]
            time_coe = float((record.time - self.start_date).days / 7 + 1)
            bias_coe = float(self.length / 7 + 1)*(self.length / 7 + 2)/2
            score += time_coe/bias_coe*base_score

        return score*100