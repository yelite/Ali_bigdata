#coding=utf-8

from datetime import date, timedelta

from db import Session
from base import Data
from model import Customer, Brand
from helper import record_aggregate

div_n = 17
breaks = [date(2012, 4, 15) + i*timedelta(7) for i in range(div_n+1)]
mean_coe = 1.0/(div_n-1)
# TODO need an elegant way to handle it


session = Session()

CUR_COE = 1.1
PP_COE = 0.4
def train_brand(brand):
    records = list()
    for i in range(div_n):
        records.append(session.query(Data).filter(Data.brand_id == brand.id,
                                                  Data.time >= breaks[i],
                                                  Data.time < breaks[i + 1]).all())
    data = map(record_aggregate, records)
    if reduce(lambda x, y: x+y[1], data, 0) == 0:
        return

    score = 0
    pp = 0
    for i in range(div_n-1):
        if data[i][1] == 0 or data[i][0]+data[i+1][0] == 0:
            continue
        score += mean_coe * (data[i+1][1])/(data[i][0]+CUR_COE*data[i+1][0])
        pp += mean_coe * PP_COE * (data[i+1][1])/(data[i][1])
    brand.click_purchase = score
    brand.purchase_purchase = pp


def train_customer(customer):
    records = list()
    for i in range(div_n):
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
    customer.purchase = min(s/3.5, p_strength/1.4)

    score = 0
    for i in range(div_n-1):
        if data[i][0]+data[i+1][0] == 0:
            continue
        score += mean_coe * (data[i+1][1])/(data[i][0]+CUR_COE*data[i+1][0])
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
