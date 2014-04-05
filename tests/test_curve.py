#coding=utf-8

from evaluation import evaluate_curve as evaluate
from models import models
import matplotlib.pyplot as plt
import numpy as np
from scipy.stats import gaussian_kde


def draw_density(data):
    density = gaussian_kde(data)
    xs = np.linspace(0, 40, 400)
    density.covariance_factor = lambda : 0.1
    density._compute_covariance()
    plt.plot(xs, density(xs))


def rev_cum(xs, data):
    rv = []
    for i in xs:
        data = filter(lambda x: x >= i, data)
        rv.append(len(data))
    return np.array(rv)


def check(session, p):
    rv = p(session, test=True).calculate_score()
    hit_val, miss_val = evaluate(rv)

    xs = np.linspace(0, 40, 400)

    all_val = hit_val[:]
    all_val.extend(miss_val)

    cum_val = [rev_cum(xs, data)
               for data in [hit_val, miss_val, all_val]]

    plt.subplot('221')
    map(draw_density, [hit_val, miss_val, all_val])
    plt.subplot('222')
    draw_density(hit_val)
    plt.subplot('223')

    for i in cum_val:
        plt.plot(xs, i)

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