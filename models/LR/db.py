#coding=utf-8

import os

from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker

package_dic = os.path.split(os.path.realpath(__file__))[0]

TRAIN_DB_FILE = os.path.join(package_dic, 'train.db')

engine = create_engine('sqlite:///{}'.format(TRAIN_DB_FILE))
Session = sessionmaker(bind=engine)
s = Session()
