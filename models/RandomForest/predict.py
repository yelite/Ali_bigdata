#coding=utf-8

from datetime import timedelta
import os

from sklearn.linear_model import LogisticRegression
import numpy as np

from .db import s
from .model import Brand, Customer
from models.base import BasePredictor
from train import INV
from helper import root_dic


package_dic = os.path.split(os.path.realpath(__file__))[0]


class Predictor(BasePredictor):
    def __init__(self, ext_session, session=s,
                 static_data=None, test=False):
        super(Predictor, self).__init__(ext_session, static_data, test)

        brands = session.query(Brand).all()
        self.brands = {x.id: x for x in brands}
        customers = session.query(Customer).all()
        self.customers = {x.id: x for x in customers}

        self.breaks = [self.start_date + i * timedelta(INV)
                       for i in range(self.length / INV + 1)]

        self.estimator = LogisticRegression(penalty='l1',
                                            fit_intercept=False,
                                            C=0.5,
                                            class_weight='auto')
        self.all = float(len(self.customers.keys()))

        if test:
            self.path = os.path.join(root_dic, 'tests/data/LR')
        else:
            self.path = package_dic

        with open(os.path.join(self.path, 'data.txt')) as f:
            data = f.readlines()
            self.data = np.array(map(lambda x: map(int, x.split('\t')), data))

        with open(os.path.join(self.path, 'freeze_data.txt')) as f:
            data = f.readlines()
            self.freeze_data = np.array(map(lambda x: map(int, x.split('\t')), data))

        print('Training')
        self.begin()
        self.train()
        print('Done')

    def predict(self, threshold=0.68):
        suggestion = self.calculate_score()
        rv = {int(k): {int(l) for l, p in v.items() if p > threshold}
              for k, v in suggestion.items()}

        p_count = 0
        for id, brands in rv.items():
            p_count += len(brands)
        print(p_count)

        return rv

    def calculate_score(self):
        self.begin()
        data = self.freeze_data

        output = self.estimator.predict_proba(data[:, 2:])[:, 1]
        output = np.column_stack((data[:, :2], output))
        rv = {}
        for u_id, b_id, score in output:
            rv.setdefault(u_id, {})
            rv[u_id][b_id] = score

        return rv

    def train(self):
        X, y = self.data[..., :-1], self.data[..., -1]
        print 'Fitting'
        self.estimator.fit(X, y)
        print 'Done'
