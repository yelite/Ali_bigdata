#coding=utf-8

import os

from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker

from helper import root_dic

DB_FILE = os.path.join(root_dic, 'data/data.db')

engine = create_engine('sqlite:///{}'.format(DB_FILE))
Session = sessionmaker(bind=engine)
s = Session()
