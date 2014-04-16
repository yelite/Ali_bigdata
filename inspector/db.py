#coding=utf-8

import os

from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker

root_dic = os.path.split(os.path.realpath(__file__))[0]
root_dic = os.path.join(root_dic, '..')

DB_FILE = os.path.join(root_dic, 'data/data.db')

engine = create_engine('sqlite:///{}'.format(DB_FILE))
Session = sessionmaker(bind=engine)
s = Session()
