#coding=utf-8

from model import Data, Brand, Customer
from db import Session
from datetime import date, timedelta
from train import record_aggregate
from math import ceil
import time

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
    return 34*cp*data[0] + 1.5*pp*data[1] + 1.5*data[2] + 1.8*data[3]


def judge_purchase(customer, brand_score):
    limit = int(ceil(customer.purchase-0.1))
    brands = sorted(brand_score, key=brand_score.get, reverse=True)
    return brands[:limit]


def forecast(customer):
    brand_id = session.execute("SELECT DISTINCT brand_id FROM DATA WHERE user_id=:id",
                               {'id': customer.id}).fetchall()
    brand_id = map(lambda x: x[0], brand_id)

    print customer.id

    brand_score = dict()
    for b in brand_id:
        brand = session.query(Brand).get(b)
        score = calculate_score(customer, brand, date(2012, 8, 16))
        brand_score[b] = score

    brands = judge_purchase(customer, brand_score)

    return customer.id, brands


def write_file(name, rv):
    f = open('output/{}.txt'.format(name), mode='w')
    for l in rv:
        name = map(str, l[1])
        id = str(l[0])
        f.write(id+'\t'+','.join(name))
        f.write('\n')
    f.close()


def main():
    c = session.query(Customer).all()
    rv = map(forecast, c)

    timestamp = time.strftime('%m_%d_%H_%M', time.localtime())
    write_file(timestamp, rv)


if __name__ == '__main__':
    main()