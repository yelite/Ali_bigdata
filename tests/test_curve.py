#coding=utf-8

import matplotlib.pyplot as plt
import numpy as np
from scipy.stats import gaussian_kde

from evaluation import evaluate_curve as evaluate
from models import models


def draw_density(data, xs):
    density = gaussian_kde(data)
    density.covariance_factor = lambda: 0.01
    density._compute_covariance()
    plt.plot(xs, density(xs))


def rev_cum(xs, data):
    rv = []
    for i in xs:
        data = filter(lambda x: x >= i, data)
        rv.append(float(len(data)))
    return np.array(rv)


def check(session, p, scale=None):
    if not scale:
        scale = [0, 40]
    rv = p(session, test=True).calculate_score()
    hit_val, miss_val = evaluate(rv)

    xs = np.linspace(scale[0], scale[1], (scale[1]-scale[0]) * 100)

    all_val = hit_val[:]
    all_val.extend(miss_val)

    cum_val = [rev_cum(xs, data)
               for data in [hit_val, miss_val, all_val]]

    plt.subplot('221')
    map(lambda x: draw_density(x, xs), [hit_val, miss_val, all_val])
    plt.subplot('222')
    plt.plot(xs, cum_val[2])
    plt.subplot('223')
    plt.plot(xs, np.divide(np.array(cum_val[0]),
                           np.array(cum_val[2])))
    plt.subplot('224')
    plt.plot(xs, cum_val[0])

    plt.show()


def test_simple_full_training(test_session):
    m = models['Simple']
    check(test_session, m.Predictor)


def test_cf_full_training(test_session):
    m = models['CF']
    check(test_session, m.Predictor)


def test_causal_full_training(test_session):
    m = models['Causal']
    check(test_session, m.Predictor)


def test_lr_full_training(test_session):
    m = models['LR']
    check(test_session, m.Predictor, scale=[0.55,1])


def test_rf_full_training(test_session):
    m = models['RandomForest']
    check(test_session, m.Predictor, scale=[0.4,1])