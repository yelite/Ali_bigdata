#coding=utf-8

import csv
import codecs
from datetime import date

from db import s
from models import Data
from models.Trivial.model import Customer, Brand


def replace_chn_char():
    f = codecs.open('t_alibaba_data.csv', mode='r', encoding='GBK')
    nf = open('data.csv', mode='w')

    for line in f:
        line = line.replace(u'月', '/')
        line = line.replace(u'日', '')
        nf.write(line)

    f.close()
    nf.close()


def _store(v):
    v['user_id'] = int(v['user_id'])
    v['brand_id'] = int(v['brand_id'])
    v['action'] = int(v['action'])
    m, d = v['time'].split('/')
    v['time'] = date(year=2012, month=int(m), day=int(d))
    t = Data(**v)
    s.add(t)


def store():
    f = open('data.csv', mode='r')
    data = csv.DictReader(f)
    map(_store, data)
    s.commit()


def _generate_test_data(c):
    b = s.execute('SELECT DISTINCT brand_id FROM DATA WHERE user_id=:id '
                  'and time>"2012-07-15"'
                  'and action=1',
                  {'id': c.id}).fetchall()
    b = map(lambda x: x[0], b)
    return c.id, b


def generate_test_data():
    c = s.query(Customer).all()
    rv = map(_generate_test_data, c)
    f = open('test/test_data.txt', mode='w')
    for l in rv:
        name = map(str, l[1])
        id = str(l[0])
        f.write(id + '\t' + ','.join(name))
        f.write('\n')
    f.close()


def _generate_user_brand_data(c):
    b = s.execute('SELECT DISTINCT brand_id FROM DATA WHERE user_id=:id '
                  'and time<"2012-08-16"',
                  {'id': c.id}).fetchall()
    b = map(lambda x: x[0], b)
    return c.id, b


def generate_user_brand_data():
    c = s.query(Customer).all()
    rv = map(_generate_user_brand_data, c)
    f = open('user_brand.txt', mode='w')
    for l in rv:
        name = map(str, l[1])
        id = str(l[0])
        f.write(id + '\t' + ','.join(name))
        f.write('\n')
    f.close()


def _generate_brand_user_data(c):
    b = s.execute('SELECT DISTINCT user_id FROM DATA WHERE brand_id=:id '
                  'and time<"2012-08-16"',
                  {'id': c.id}).fetchall()
    b = map(lambda x: x[0], b)
    return c.id, b


def generate_brand_user_data():
    c = s.query(Brand).all()
    rv = map(_generate_brand_user_data, c)
    f = open('brand_user.txt', mode='w')
    for l in rv:
        name = map(str, l[1])
        id = str(l[0])
        if not name:
            continue
        f.write(id + '\t' + ','.join(name))
        f.write('\n')
    f.close()


if __name__ == '__main__':
    generate_brand_user_data()
