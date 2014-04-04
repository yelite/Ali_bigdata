#coding=utf-8

from .predict import Predictor

def full_test(session):
    rv = Predictor(session, test=True).predict(threshold=3)
    return rv