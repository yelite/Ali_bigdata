#coding=utf-8

import os

from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker

print('testing!')

MAIN_DIC = os.path.split(os.path.realpath(__file__))[0]
DB_FILE = os.path.join(MAIN_DIC, 'test_data.db')

engine = create_engine('sqlite:///{}'.format(DB_FILE))
Session = sessionmaker(bind=engine)
