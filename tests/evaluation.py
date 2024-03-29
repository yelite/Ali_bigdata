#coding=utf-8

import os

FILE_DIC = os.path.split(os.path.realpath(__file__))[0]


def read_result():
    f = open(os.path.join(FILE_DIC, 'data/real.txt'))
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


def evaluate(p_rv):
    print('Evaluating...')
    p_count = 0
    for brands in p_rv.values():
        p_count += len(brands)

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


def evaluate_curve(p_rv):
    r_rv = read_result()[1]
    hit_val = []
    miss_val = []
    for user, brands in p_rv.items():
        for brand, score in brands.items():
            if score > 40:
                score = 40
            if brand in r_rv[user]:
                hit_val.append(score)
            else:
                miss_val.append(score)

    return hit_val, miss_val




