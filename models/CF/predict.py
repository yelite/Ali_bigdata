#coding=utf-8

import os
from datetime import timedelta

from sqlalchemy import desc

from .db import s
from models.data import Data
from models.static import StaticData
from .model import Brand, Customer
from helper import record_aggregate


class Predictor:
    def __init__(self, ext_session, session=s, test=False):
        self.ext_session = ext_session
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
        self.brand_user = self.static_data.brand_user

    def predict(self, threshold=0.8):
        self.count = 0
        suggestion = {k: self.calculate_score(k) for k in self.customers.keys()}

        rv = {k: {l for l, s in v.items() if s > threshold}
              for k, v in suggestion.items()}
        p_count = 0
        for id, brands in rv.items():
            p_count += len(brands)
        print(p_count)
        return rv

    def calculate_score(self, user_id):
        brand_score = dict()
        brands = self.user_brand.get(user_id, frozenset())
        if not brands:
            return brand_score
        similar_users = reduce(lambda x, y: x.union(y),
                               map(self.brand_user.get, brands), set())
        users_score = {k: self.calculate_similarity(user_id, k)
                       for k in similar_users}
        users_score.pop(user_id)
        for u, v in users_score.items():
            new_brands = self.user_brand.get(u) - brands
            for b in new_brands:
                brand_score.setdefault(b, 0.0)
                brand_score[b] += v
        self.done()
        return brand_score

    def calculate_similarity(self, a, b):
        a_s = self.user_brand.get(a)
        b_s = self.user_brand.get(b)
        overlap = len(a_s & b_s)
        total = len(a_s | b_s)
        score = (overlap / float(total)) ** 0.5
        return score if score > 0.3 else 0.0

    def done(self):
        self.count += 1
        if self.count % 128 == 0:
            print self.count / self.all