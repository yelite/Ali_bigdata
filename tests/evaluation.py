#coding=utf-8

import os

FILE_DIC = os.path.split(os.path.realpath(__file__))[0]


def read_result():
    f = open(os.path.join(FILE_DIC, 'real.txt'))
    rv = {}
    count = 0
    for l in f:
        name, brands = l.split('\t')
        brands = brands.strip()
        if not brands:
            rv[int(name)] = set()
            continue
        brands = map(int, brands.split(','))
        count += len(brands)
        rv[int(name)] = set(brands)
    f.close()
    return count, rv


def check(p_rv, c_rv):
    count = 0
    for key, value in p_rv.items():
        count += len(value.intersection(c_rv.get(key, set())))
    return count


def evaluate(prediction, flag='full'):
    print('Evaluating...')
    p_count = 0
    p_rv = {}
    for id, brands in prediction:
        p_count += len(brands)
        p_rv[id] = set(brands)

    r_count, r_rv = read_result()

    hit_count = check(p_rv, r_rv)
    hit_count = float(hit_count)
    precision = hit_count / p_count
    recall = hit_count / r_count
    f1_score = 2 * hit_count / (p_count + r_count)

    report_data = {'hit_count': hit_count,
                   'p_count': p_count,
                   'r_count': r_count,
                   'precision': precision,
                   'recall': recall,
                   'score': f1_score}

    return report_data