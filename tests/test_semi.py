#coding=utf-8

from datetime import date

from evaluation import evaluate
from models.Trivial.predict import predict
from report import report_static_test


def test_semi_training(test_session):
    rv = predict(date(2012, 7, 16))
    report_data = evaluate(rv)
    print(report_static_test(report_data, flag='Semi'))