#coding=utf-8

from datetime import date

from db import Session
from model import Data, Customer, Brand


breaks = [date(2012, 4, 15),
          date(2012, 5, 15),
          date(2012, 6, 15),
          date(2012, 7, 15),
          date(2012, 8, 15), ]


def record_aggregate(records):
    rv = [0] * 4
    for i in records:
        rv[i.action] += 1
    return rv


session = Session()

ZERO_MOD = 0.1
CUR_COE = 0.7
PP_COE = 0.2
def train_brand(brand):
    records = list()
    for i in range(4):
        records.append(session.query(Data).filter(Data.brand_id == brand.id,
                                                  Data.time >= breaks[i],
                                                  Data.time < breaks[i + 1]).all())
    data = map(record_aggregate, records)
    if reduce(lambda x, y: x+y[1], data, 0) == 0:
        return

    score = 0
    pp = 0
    for i in range(3):
        score += 0.334 * (data[i+1][1])/(data[i][0]+CUR_COE*data[i+1][0]+ZERO_MOD)
        pp += 0.334 * PP_COE * (data[i+1][1])/(data[i][1]+ZERO_MOD)
    brand.click_purchase = score
    brand.purchase_purchase = pp


def train_customer(customer):
    records = list()
    for i in range(4):
        records.append(session.query(Data).filter(Data.user_id == customer.id,
                                                  Data.time >= breaks[i],
                                                  Data.time < breaks[i + 1]).all())
    data = map(record_aggregate, records)
    unique_dict = dict()
    s = reduce(lambda x, y: x+y[1], data, 0)
    if s == 0:
        return

    p_strength = 0
    for i in records:
        for j in i:
            if j.action == 1 and j.brand_id not in unique_dict:
                p_strength += 1
                unique_dict[j.brand_id] = 0
    customer.purchase = min(s/4.0, p_strength/1.7)

    score = 0
    for i in range(3):
        score += 0.334 * (data[i+1][1])/(data[i][0]+CUR_COE*data[i+1][0]+ZERO_MOD)
    customer.click_purchase = score


def train():
    # TODO save memory
    brands = session.query(Brand).all()
    map(train_brand, brands)

    customers = session.query(Customer).all()
    map(train_customer, customers)

    session.commit()


if __name__ == "__main__":
    train()
