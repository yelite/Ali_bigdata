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

    xs = np.linspace(scale[0], scale[1], (scale[1] - scale[0]) * 100)

    all_val = hit_val[:]
    all_val.extend(miss_val)

    cum_val = [np.array(rev_cum(xs, data))
               for data in [hit_val, miss_val, all_val]]

    plt.subplot('221')
    map(lambda x: draw_density(x, xs), [hit_val, miss_val, all_val])
    plt.subplot('222')
    plt.plot(xs, 2*cum_val[0]/(cum_val[2] + 1378))
    plt.subplot('223')
    plt.plot(xs, np.divide(cum_val[0],
                           cum_val[2]))
    plt.subplot('224')
    plt.plot(xs, cum_val[0])

    print('Plotting')
    plt.show()


def test_simple_full_training(test_session):
    m = models['Simple']
    check(test_session, m.Predictor, [0, 4])


def test_cf_full_training(test_session):
    m = models['CF']
    check(test_session, m.Predictor)


def test_causal_full_training(test_session):
    m = models['Causal']
    check(test_session, m.Predictor)


def test_rf_full_training(test_session):
    m = models['RandomForest']
    check(test_session, m.Predictor, scale=[0.05, 0.5])


def test_svm_full_training(test_session):
    m = models['SVM']
    check(test_session, m.Predictor, [0, 1])


def test_lr_full_training(test_session):
    m = models['LR']
    check(test_session, m.Predictor, scale=[0.4, 1])


