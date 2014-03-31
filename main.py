#coding=utf-8

import time

from models.Trivial.model import Customer
from db import Session
from models.Trivial.predict import predict


session = Session()


def write_file(name, rv):
    f = open('output/{}.txt'.format(name), mode='w')
    for l in rv:
        if not l[1]:
            continue
        name = map(str, l[1])
        id = str(l[0])
        f.write(id+'\t'+','.join(name))
        f.write('\n')
    f.close()


def main():
    rv = predict()

    p_count = 0
    for id, brands in rv:
        p_count += len(brands)

    print('Prediction: {}'.format(p_count))

    timestamp = time.strftime('%m_%d_%H_%M', time.localtime())
    write_file(timestamp+'_'+str(p_count), rv)


if __name__ == '__main__':
    main()