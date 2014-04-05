#coding=utf-8

from datetime import date

from _db import s
from evaluation import evaluate
from models import models
from report import report_static_test

def test_simple_full_training(test_session):
    m = models['Simple']
    rv = m.Predictor(test_session, test=True).predict()
    report_data = evaluate(rv)
    print(report_static_test(report_data, flag='Full'))


def test_cf_full_training(test_session):
    m = models['CF']
    rv = m.Predictor(test_session, test=True).predict()
    report_data = evaluate(rv)
    print(report_static_test(report_data, flag='Full'))


def test_causal_full_training(test_session):
    m = models['Causal']
    rv = m.Predictor(test_session, test=True).predict()
    report_data = evaluate(rv)
    print(report_static_test(report_data, flag='Full'))


def test_mixed_full_training(test_session):
    target = {'Simple': 20,
              'Causal': 1.4,
              'CF': 0.4}

    all = [models[k].Predictor(test_session, test=True).predict(threshold=v)
           for k, v in target.items()]

    rv = {}
    for r in all:
        for k, v in r.items():
            rv.setdefault(k, set())
            rv[k] |= v

    report_data = evaluate(rv)
    print(report_static_test(report_data, flag='Full'))



