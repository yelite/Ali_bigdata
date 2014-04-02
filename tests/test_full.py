#coding=utf-8

from datetime import date

from _db import s
from evaluation import evaluate
from models import models
from report import report

def test_full_training(session):
    t = models['Causal']
    rv = t.Predictor(s, test=True).predict()
    report_data = evaluate(rv)
    print(report(report_data, flag='Full'))


