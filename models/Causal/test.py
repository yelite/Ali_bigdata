#coding=utf-8

import os
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker
from helper import root_dic
from .db import s as full_session
from predict import Predictor


TRAIN_DB_FILE = os.path.join(root_dic, 'tests/data/Causal.db')

engine = create_engine('sqlite:///{}'.format(TRAIN_DB_FILE))
Session = sessionmaker(bind=engine)
partial_session = Session()

def full_test(session):
    rv = Predictor(session, test=True).predict(threshold=0.8)
    return rv