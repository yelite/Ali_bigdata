#coding=utf-8
from datetime import date, timedelta
from math import ceil

from model import Data, Brand
from db import Session
from train import record_aggregate

session = Session()

def calculate_score(customer, brand, break_date):
    dt = timedelta(30)
    cp = 0.4*max(brand.click_purchase, customer.click_purchase)
    cp += 0.6*min(brand.click_purchase, customer.click_purchase)
    pp = brand.purchase_purchase

    history = session.query(Data).filter(Data.user_id==customer.id,
                                         Data.brand_id==brand.id,
                                         Data.time >= break_date - dt,
                                         Data.time < break_date).all()
    data = record_aggregate(history)
    return 30*cp*data[0] + 1.5*pp*data[1] + 1.5*data[2] + 2.8*data[3]


def judge_purchase(customer, brand_score):
    limit = int(ceil(customer.purchase-0.1))
    brands = sorted(brand_score, key=brand_score.get, reverse=True)
    return brands[:limit]

COUNT = 0
def predict(customer, predict_time=date(2012, 8, 16)):
    brand_id = session.execute("SELECT DISTINCT brand_id FROM DATA WHERE user_id=:id",
                               {'id': customer.id}).fetchall()
    brand_id = map(lambda x: x[0], brand_id)

    global COUNT
    COUNT += 1
    try:
        index = [170, 340, 520, 690].index(COUNT)
    except ValueError:
        pass
    else:
        print(str(20*(index+1))+'%...')

    brand_score = dict()
    for b in brand_id:
        brand = session.query(Brand).get(b)
        score = calculate_score(customer, brand, predict_time)
        brand_score[b] = score

    brands = judge_purchase(customer, brand_score)

    return customer.id, brands