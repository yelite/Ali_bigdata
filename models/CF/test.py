#coding=utf-8

from .predict import Predictor


def full_test(session):
    rv = Predictor(session, test=True).predict()
    return rv


def hit_curve_test(session):
    pass
