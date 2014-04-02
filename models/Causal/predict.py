#coding=utf-8

import os
from db import s
from model import Data
from .train_model import Brand, Customer
from .train import INV, START_DATE
from datetime import timedelta
from helper import root_dic
from helper import record_aggregate
from sqlalchemy import desc


class Predictor:
    def __init__(self, session, test=False):
        self.ext_session = session
        self.end_date = session.query(Data.time).order_by(desc(Data.time)).first()[0]
        self.test = test
        self.load()

    def load(self):
        brands = s.query(Brand).all()
        self.brands = {x.id: x for x in brands}
        customers = s.query(Customer).all()
        self.customers = {x.id: x for x in customers}
        self.data_query = self.ext_session.query(Data)

        name = 'data/user_brand{}.txt'.format('_test' if self.test else '')
        self.user_brand = self.init_user_brand(os.path.join(root_dic, name))

    @staticmethod
    def init_user_brand(dic):
        f = open(dic)
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

    def predict(self):
        self.count = 0
        self.all = float(len(self.customers.keys()))
        return map(self._predict, self.customers.values())

    def _predict(self, c):
        brand_ids = self.user_brand.get(c.id, frozenset())
        if c.idle:
            return self._predict_idle(c, brand_ids)

        brand_score = dict()
        for b in brand_ids:
            brand = self.brands.get(b)
            score = self.calculate_score(c, brand)
            brand_score[b] = score

        brands = self.judge_purchase(c, brand_score)

        self.done()
        return c.id, brands

    def _predict_idle(self, c, brand_ids):
        dt = timedelta(2*INV)
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
        return c.id, brands

    def calculate_score(self, c, brand):
        dt = timedelta(4*INV)
        cp = c.click_purchase
        pp = brand.purchase_purchase

        history = self.data_query.filter(Data.user_id==c.id,
                                         Data.brand_id==brand.id,
                                         Data.time > self.end_date - dt,
                                         Data.time <= self.end_date).all()

        data = record_aggregate(history, unique_brand=True)
        if data[3]+data[2]-data[1]>0:
            return 1000
        return cp*data[0] + 12*pp*data[1] + cp*pp*data[0]*25

    @staticmethod
    def judge_purchase(customer, brand_score):
        limit = int(customer.purchase**1.25+1.4*customer.purchase)+1
        brands = [k for k,v in brand_score.items() if v > 2]
        brands = sorted(brands, key=brand_score.get, reverse=True)
        return brands[:limit]

    def done(self):
        self.count += 1
        if self.count % 128 == 0:
            print self.count / self.all

