#coding=utf-8

import os

from helper import root_dic

from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker

DB_FILE = os.path.join(root_dic, 'data/data.db')

engine = create_engine('sqlite:///{}'.format(DB_FILE))
Session = sessionmaker(bind=engine)
