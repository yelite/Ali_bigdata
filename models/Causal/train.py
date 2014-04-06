#coding=utf-8

from datetime import date, timedelta

from sqlalchemy import func, desc

from models.data import Data
from .db import s
from .model import Customer, Brand
from helper import record_aggregate


START_DATE = date(2012, 4, 15)
INV = 28


def calculate_cp_score(data):
    new, old = data
    if old[0] + 2 * new[0] == 0:
        return new[1] / 3.0
    return 3.0 * new[1] / (old[0] + 2 * new[0])


def calculate_pp_score(data):
    new, old = data
    if old == 0:
        return 0
    return new / float(old)


def skewed_mean(scores):
    l = len(scores)
    c = l * (l + 1) / 2
    acc = 0
    for i, s in enumerate(scores):
        acc += (i + 1) * s
    return acc / c


class Trainer:
    def __init__(self, ext_session, session=s, inv=INV):
        self.parameters = {'inv': INV}

        self.session = session

        self.end_date = ext_session.query(Data.time).order_by(desc(Data.time)).first()[0]
        self.length = self.end_date - START_DATE

        self.inv = inv
        self.mean_coe = 1.0 / (inv - 1)
        self.div = self.length.days / inv
        self.breaks = [START_DATE + i * timedelta(inv) for i in range(self.div + 1)]

        brands = self.session.query(Brand).all()
        self.brands = {x.id: x for x in brands}
        self.customers = self.session.query(Customer).all()
        self.data_query = ext_session.query(Data)
        self.ext_session = ext_session

    def train_customer(self, customer):
        records = list()
        for i in range(self.div):
            records.append(self.data_query.filter(Data.user_id == customer.id,
                                                  Data.time >= self.breaks[i],
                                                  Data.time < self.breaks[i + 1]).all())

        data = map(lambda x: record_aggregate(unique_brand=True,
                                              records=x), records)

        # Total purchase number
        s = reduce(lambda x, y: x + y[1], data, 0)
        if s == 0:
            customer.idle = True
            return

        customer.purchase = 30.0 * s / self.length.days

        cp_scores = map(calculate_cp_score, zip(data[1:], data))
        customer.click_purchase = sum(cp_scores) / len(cp_scores)

    def train_brand(self, brand):
        data = list()
        for i in range(self.div):
            t = self.ext_session.query(func.count(Data.id)).filter(Data.brand_id == brand.id,
                                                                   Data.action == 1,
                                                                   Data.time >= self.breaks[i],
                                                                   Data.time < self.breaks[i + 1]).one()
            data.append(t[0])
        pp_scores = map(calculate_pp_score, zip(data[1:], data))
        brand.purchase_purchase = sum(pp_scores) / len(pp_scores)
        if brand.purchase_purchase == 0:
            brand.idle = True

    def train_all(self):
        map(self.train_customer, self.customers)
        print('Customer parameter trained')
        map(self.train_brand, self.brands.values())
        print('Brand parameter trained')
        self.session.commit()


def train(session):
    t = Trainer(session)
    t.train_all()