#coding=utf-8

from db import Session
from main import Customer, Brand, calculate_score, judge_purchase, write_file
import time
import os
from datetime import date
session = Session()


def forecast(customer):
    brand_id = session.execute("SELECT DISTINCT brand_id FROM DATA WHERE user_id=:id",
                               {'id': customer.id}).fetchall()
    brand_id = map(lambda x: x[0], brand_id)

    print customer.id

    brand_score = dict()
    for b in brand_id:
        brand = session.query(Brand).get(b)
        score = calculate_score(customer, brand, date(2012, 7, 16))
        brand_score[b] = score

    brands = judge_purchase(customer, brand_score)

    return customer.id, brands


MAIN_DIC = os.path.split(os.path.realpath(__file__))[0]
def read_result():
    f = open(os.path.join(MAIN_DIC, 'test_rv.txt'))
    rv = {}
    count = 0
    for l in f:
        name, brands= l.split('\t')
        brands = brands.strip()
        if not brands:
            rv[int(name)] = set()
            continue
        brands = map(int, brands.split(','))
        count += len(brands)
        rv[int(name)] = set(brands)
    return count, rv


def check(p_rv, c_rv):
    count = 0
    for key, value in p_rv.items():
        count += len(value.intersection(c_rv.get(key, set())))
    return count


def main():
    c = session.query(Customer).all()
    rv = map(forecast, c)
    p_count = 0
    p_rv = {}
    for id, brands in rv:
        p_count += len(brands)
        p_rv[id] = set(brands)

    c_count, c_rv = read_result()
    print('checking...')
    hit_count = check(p_rv, c_rv)
    hit_count = float(hit_count)
    print(p_count)
    print(c_count)
    print(hit_count)
    print(hit_count/p_count)
    print(hit_count/c_count)
    print(2*hit_count/float(p_count+c_count))

if __name__ == '__main__':
    main()