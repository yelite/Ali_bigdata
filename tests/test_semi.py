#coding=utf-8

from datetime import date

from evaluation import evaluate
from models.Trivial.predict import predict
from report import report


def test_semi_training(test_session):
    rv = predict(date(2012, 7, 16))
    report_data = evaluate(rv)
    print(report(report_data, flag='Semi'))