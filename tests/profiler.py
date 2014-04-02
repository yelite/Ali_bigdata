#coding=utf-8


import profile
from datetime import date

from models.Trivial.predict import predict

profile.run('predict(date(2012, 7, 16))')