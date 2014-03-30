#coding=utf-8

import time

from model import Customer
from db import Session
from predict import predict


session = Session()


def write_file(name, rv):
    f = open('output/{}.txt'.format(name), mode='w')
    for l in rv:
        name = map(str, l[1])
        id = str(l[0])
        f.write(id+'\t'+','.join(name))
        f.write('\n')
    f.close()


def main():
    c = session.query(Customer).all()
    # p = Pool(processes=4)
    rv = map(predict, c)
    # p.close()
    # p.join()

    timestamp = time.strftime('%m_%d_%H_%M', time.localtime())
    write_file(timestamp, rv)


if __name__ == '__main__':
    main()