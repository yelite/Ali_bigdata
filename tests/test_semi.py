#coding=utf-8

from datetime import date

from model import Customer
from predict import predict
from evaluation import evaluate
from report import report


def test_semi_training(test_session):
    c = test_session.query(Customer).all()
    rv = map(lambda x: predict(x, date(2012, 7, 16)), c)
    report_data = evaluate(rv)
    print(report(report_data, flag='Semi'))