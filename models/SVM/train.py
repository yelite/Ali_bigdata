#coding=utf-8

from datetime import timedelta
import os

from sqlalchemy import desc

from models.data import Data
from .db import s
from .model import Customer, Brand
from models.static import StaticData
from helper import root_dic


package_dic = os.path.split(os.path.realpath(__file__))[0]


class Trainer:
    def __init__(self, ext_session, session=s):
        self.session = session

        brands = self.session.query(Brand).all()
        self.brands = {x.id: x for x in brands}
        self.customers = self.session.query(Customer).all()
        self.data_query = ext_session.query(Data)
        self.ext_session = ext_session

    def train_customer(self, customer):
        customer.click = self.data_query.filter(Data.user_id == customer.id,
                                                Data.action == 0).count()

    def train_brand(self, brand):
        brand.purchase = self.data_query.filter(Data.brand_id == brand.id,
                                                Data.action == 1).count()
        brand.click = self.data_query.filter(Data.brand_id == brand.id,
                                                Data.action == 0).count()


    def train_all(self):
        map(self.train_customer, self.customers)
        print('Customer parameter trained')
        map(self.train_brand, self.brands.values())
        print('Brand parameter trained')
        self.session.commit()


INV = 30


class DataTrainer:
    def __init__(self, ext_session, session=s, test=False):
        self.session = session

        brands = session.query(Brand).all()
        self.brands = {x.id: x for x in brands}
        customers = session.query(Customer).all()
        self.customers = {x.id: x for x in customers}
        self.data_query = ext_session.query(Data)

        self.all = float(len(self.customers.keys()))

        self.ext_session = ext_session

        self.end_date = ext_session.query(Data.time).order_by(desc(Data.time)).first()[0]
        self.start_date = ext_session.query(Data.time).order_by(Data.time).first()[0]
        self.length = (self.end_date - self.start_date).days

        self.static_data = StaticData(test=False)
        self.user_brand = self.static_data.user_brand
        self.brand_user = self.static_data.brand_user

        self.breaks = [self.start_date + i * timedelta(INV)
                       for i in range(self.length / INV + 1)]
        self.count = 0

        if test:
            self.path = os.path.join(root_dic, 'tests/data/LR')
        else:
            self.path = package_dic

    def train(self):
        X = self.get_data_set()

        f = open(os.path.join(self.path, 'data.txt'), 'w')
        for i in X:
            i = map(str, i)
            f.write('\t'.join(i))
            f.write('\n')
        f.close()

    def freeze(self):
        print 'Freezing'
        X = self.get_freeze_data_set()

        f = open(os.path.join(self.path, 'freeze_data.txt'), 'w')
        for i in X:
            i = map(str, i)
            f.write('\t'.join(i))
            f.write('\n')
        f.close()

    def get_data_set(self):
        X = []

        for u in self.customers.values():
            for b in self.user_brand.get(u.id, []):
                b = self.brands.get(b)
                x = self._get_data_set(u, b)
                X.extend(x)
            self.done()

        return X

    def get_freeze_data_set(self):
        X = []

        for u in self.customers.values():
            for b in self.user_brand.get(u.id, []):
                b = self.brands.get(b)
                x = self._get_freeze_data_set(u, b)
                if x:
                    X.append(x)
            self.done()

        return X

    def _get_freeze_data_set(self, c, b):
        old_purchase = self.data_query.filter(Data.user_id == c.id,
                                                  Data.brand_id == b.id,
                                                  Data.action == 1,
                                                  Data.time >= self.end_date - timedelta(INV),
                                                  Data.time < self.end_date).order_by(desc(Data.time)).first()
        if old_purchase:
            t_limit = old_purchase.time
        else:
            t_limit = self.end_date - timedelta(INV)

        click = self.data_query.filter(Data.user_id == c.id,
                                       Data.brand_id == b.id,
                                       Data.action == 0,
                                       Data.time > t_limit,
                                       Data.time <= self.end_date).count()

        cart = self.data_query.filter(Data.user_id == c.id,
                                      Data.brand_id == b.id,
                                      Data.action == 2 or Data.action == 3,
                                      Data.time >= t_limit,
                                      Data.time < self.end_date)

        cart = cart.order_by(desc(Data.time)).first()
        f = 1 if cart else 0

        return [c.id, b.id, click, f, c.click, c.purchase, b.purchase, b.purchase]

    def _get_data_set(self, c, b):
        x = []
        for i in range(self.length / INV - 1):
            old_purchase = self.data_query.filter(Data.user_id == c.id,
                                                  Data.brand_id == b.id,
                                                  Data.action == 1,
                                                  Data.time >= self.breaks[i],
                                                  Data.time < self.breaks[i + 1]).order_by(desc(Data.time)).first()
            if old_purchase:
                t_limit = old_purchase.time
            else:
                t_limit = self.breaks[i]

            click = self.data_query.filter(Data.user_id == c.id,
                                           Data.brand_id == b.id,
                                           Data.action == 0,
                                           Data.time >= t_limit,
                                           Data.time < self.breaks[i + 1]).count()

            purchase = self.data_query.filter(Data.user_id == c.id,
                                              Data.brand_id == b.id,
                                              Data.action == 1,
                                              Data.time >= self.breaks[i + 1],
                                              Data.time < self.breaks[i + 2]).count()

            purchase = 1 if purchase else 0

            cart = self.data_query.filter(Data.user_id == c.id,
                                          Data.brand_id == b.id,
                                          Data.action == 2 or Data.action == 3,
                                          Data.time >= t_limit,
                                          Data.time < self.breaks[i + 1])

            cart = cart.order_by(desc(Data.time)).first()
            f = 1 if cart else 0

            x.append([click, f, c.click, c.purchase, b.click, b.purchase, purchase])
        return x

    def done(self):
        self.count += 1
        if self.count % 2 == 0:
            print self.count / self.all


def train(session):
    Trainer(session).train_all()
    t = DataTrainer(session)
    t.train()
    t.freeze()


