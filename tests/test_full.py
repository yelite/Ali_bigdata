#coding=utf-8

from datetime import date

from _db import s
from evaluation import evaluate
from models import models
from report import report

def test_full_training(test_session):
    t = models['Causal']
    rv = t.test.full_test(test_session)
    report_data = evaluate(rv)
    print(report(report_data, flag='Full'))


