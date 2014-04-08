#coding=utf-8

from flask import Flask, abort, jsonify

from db import s
from models.static import StaticData
from models.base import Data
from datetime import datetime

app = Flask(__name__)
app.static_data = StaticData()


def unix_time(dt):
    epoch = datetime.utcfromtimestamp(0)
    delta = dt - epoch
    return delta.total_seconds()


def unix_time_millis(dt):
    return unix_time(dt) * 1000


def data_aggregate(d):
    rv = dict()
    return rv


@app.route('/user')
def get_user_list():
    return jsonify(app.static_data.user_brand.keys())


@app.route('/user/<int:uid>')
def get_user_data(uid):
    rv = s.query(Data).filter(Data.user_id == uid).all()
    return jsonify(data_aggregate(rv))


@app.route('/user/<int:uid>/brand')
def get_user_brand_list(uid):
    return jsonify(app.static_data.user_brand.get(uid))


@app.route('/user/<int:uid>/brand/<int:bid>')
def get_user_brand_data(uid, bid):
    pass


@app.route('/brand')
def get_brand_list():
    return jsonify(app.static_data.brand_user.keys())


@app.route('/brand/<int:bid>')
def get_brand_data(bid):
    rv = s.query(Data).filter(Data.brand_id == bid).all()
    return jsonify(data_aggregate(rv))


@app.route('/brand/<int:bid>/user')
def get_brand_user_list(bid):
    return jsonify(app.static_data.user_brand.get(bid))


@app.route('/brand/<int:bid>/user/<int:uid>')
def get_brand_user_data(uid, bid):
    pass
