#coding=utf-8

import time

from db import s
from models import models


def write_file(name, rv):
    f = open('output/{}.txt'.format(name), mode='w')
    for k, v in rv.items():
        if not v:
            continue
        name = map(str, v)
        id = str(k)
        f.write(id + '\t' + ','.join(name))
        f.write('\n')
    f.close()


def main():
    target = {'LR': 0.89,
              'Simple': 13.4,
              'Causal': 3.4,
              'RandomForest': 0.24}
    print(target.keys())
    all = [models[k].Predictor(s).predict(threshold=v)
           for k, v in target.items()]

    rv = {}
    for r in all:
        for k, v in r.items():
            rv.setdefault(k, set())
            rv[k] |= v

    p_count = 0
    for id, brands in rv.items():
        p_count += len(brands)

    print('Prediction: {}'.format(p_count))

    timestamp = time.strftime('%m_%d_%H_%M', time.localtime())
    write_file(timestamp + '_' + str(p_count), rv)


if __name__ == '__main__':
    main()