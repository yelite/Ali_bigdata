#coding=utf-8

from datetime import date

from model import Customer
from predict import predict
from evaluation import evaluate
from report import report


def test_full_training(session):
    c = session.query(Customer).all()
    rv = map(lambda x: predict(x, date(2012, 7, 16)), c)
    report_data = evaluate(rv)
    print(report(report_data, flag='Full'))


