#coding=utf-8
from datetime import date, timedelta
from math import ceil

from base import Data
from model import Brand, Customer
from db import Session
from helper import record_aggregate
from base import static_data


session = Session()


def calculate_score(customer, brand, break_date):
    dt = timedelta(40)
    cp = 28.6*max(brand.click_purchase, customer.click_purchase)
    cp += 8.8*min(brand.click_purchase, customer.click_purchase)
    pp = brand.purchase_purchase

    history = session.query(Data).filter(Data.user_id==customer.id,
                                         Data.brand_id==brand.id,
                                         Data.time >= break_date - dt,
                                         Data.time < break_date).all()
    data = record_aggregate(history)
    return cp*data[0] - 12.8*pp*data[1] + 0.2*data[2] + 1.4*data[3]


def judge_purchase(customer, brand_score):
    limit = int(ceil(customer.purchase)) + 3
    brands = [k for k,v in brand_score.items() if v > 2.8]
    brands = sorted(brands, key=brand_score.get, reverse=True)
    return brands[:limit]




COUNT = 0
def _predict(customer, predict_time=date(2012, 8, 16)):
    brand_id = get_user_brand(customer.id)

    # TODO replace it with a thread safe method
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
        brand = Brand.get_by_id(session, b)
        score = calculate_score(customer, brand, predict_time)
        brand_score[b] = score

    brands = judge_purchase(customer, brand_score)

    return customer.id, brands


def predict(predict_time=date(2012, 8, 16)):
    c = session.query(Customer).first()
    # p = Pool(processes=4)
    rv = [_predict(x, predict_time) for x in [c]]
    # p.close()
    # p.join()
    return rv