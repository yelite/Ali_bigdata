#coding=utf-8

from .db import s
from models.data import Data
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

    def predict(self, threshold=2.2):
        self.count = 0
        suggestion = self.calculate_score()

        rv = {int(k): {int(l) for l, s in v.items() if s > threshold}
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
        default_table = {0: 1,
                         1: 15,
                         2: 10,
                         3: 20}

        all = record_aggregate(history, unique_date=True)
        if all[1] > 1:
            default_table[1] = 25
            default_table[2] = default_table[3] = 6

        score_table = default_table.copy()

        for record in history:
            base_score = score_table[record.action]

            # Dynamic suppressing
            if record.action == 2 or record.action == 3:
                score_table[1] -= score_table[record.action]
            elif record.action == 1:
                score_table[1] = default_table[1]

            time_coe = float((record.time - self.start_date).days / 7 + 1)
            bias_coe = float(self.length / 7 + 1) * (self.length / 7 + 2) / 2
            score += time_coe / bias_coe * base_score

        return score