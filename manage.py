#coding=utf-8

import sys

from db import engine, Session
from model import Base, Customer, Brand


def create():
    Base.metadata.create_all(engine)


def init_id():
    s = Session()
    rv = s.execute('select distinct user_id from data')
    obj = map(lambda x: Customer(id=x[0]), rv.fetchall())
    s.add_all(obj)

    rv = s.execute('select distinct brand_id from data')
    obj = map(lambda x: Brand(id=x[0]), rv.fetchall())
    s.add_all(obj)

    s.commit()

if __name__ == '__main__':
    try:
        cmd = sys.argv[1]
    except IndexError:
        cmd = None

    if cmd == 'create':
        create()
    else:
        print('support method: create')
