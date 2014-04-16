#coding=utf-8

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


def test_lr_full_training(test_session):
    m = models['LR']
    rv = m.Predictor(test_session, test=True).predict()
    report_data = evaluate(rv)
    print(report_static_test(report_data, flag='Full'))


def test_rf_full_training(test_session):
    m = models['RandomForest']
    rv = m.Predictor(test_session, test=True).predict()
    report_data = evaluate(rv)
    print(report_static_test(report_data, flag='Full'))


def test_svm_full_training(test_session):
    m = models['SVM']
    rv = m.Predictor(test_session, test=True).predict()
    report_data = evaluate(rv)
    print(report_static_test(report_data, flag='Full'))


def test_mixed_full_training(test_session):
    target = {'LR': 0.82,
              'Simple': 18,
              'Causal': 4}

    all = [models[k].Predictor(test_session, test=True).predict(threshold=v)
           for k, v in target.items()]

    rv = {}
    for r in all:
        for k, v in r.items():
            rv.setdefault(k, set())
            rv[k] |= v

    report_data = evaluate(rv)
    print(report_static_test(report_data, flag='Full'))



