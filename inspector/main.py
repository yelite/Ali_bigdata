#coding=utf-8

from datetime import date, timedelta

from flask import Flask, jsonify, render_template, g

from models.static import StaticData
from models.base import Data
from json_ import json_patch

app = Flask(__name__)
json_patch(app)
app.static_data = StaticData()

start_date = date(2012, 4, 12)
end_date = date(2012, 8, 18)
length = (end_date - start_date).days
date_range = [start_date + i * timedelta(1) for i in range(length)]


def data_aggregate(d):
    rv = dict()

    for i in date_range:
        rv.setdefault(i, [0] * 4)

    for i in d:
        rv[i.time][i.action] += 1
    t = sorted(rv.keys())
    data = [[], [], [], []]
    for i in range(4):
        for j in t:
            data[i].append(rv[j][i])
    time = map(lambda x: ' '.join((str(x.month),
                                   str(x.day),
                                   str(x.year))), t)
    return {'time': time,
            'click': data[0],
            'purchase': data[1],
            'save': data[2],
            'cart': data[3]}


def get_session():
    session = getattr(g, '_session', None)
    if session is None:
        from db import Session

        session = g._session = Session()
    return session


@app.teardown_appcontext
def close_session(exception):
    session = getattr(g, '_session', None)
    if session:
        # noinspection PyUnresolvedReferences
        session.close()


@app.route('/')
def index():
    return render_template('index.html')


@app.route('/summary')
def summary():
    return jsonify({'u_b': app.static_data.user_brand,
                    'b_u': app.static_data.brand_user})


@app.route('/user')
def get_user_list():
    return jsonify({'users': app.static_data.user_brand.keys()})


@app.route('/user/<int:uid>')
def get_user_data(uid):
    s = get_session()
    rv = s.query(Data).filter(Data.user_id == uid).all()
    return jsonify(data_aggregate(rv))


@app.route('/user/<int:uid>/brand')
def get_user_brand_list(uid):
    return jsonify({'brands': app.static_data.user_brand.get(uid)})


@app.route('/user/<int:uid>/brand/<int:bid>')
def get_user_brand_data(uid, bid):
    s = get_session()
    rv = s.query(Data).filter(Data.user_id == uid,
                              Data.brand_id == bid).all()
    return jsonify(data_aggregate(rv))


@app.route('/brand')
def get_brand_list():
    return jsonify({'brands': app.static_data.brand_user.keys()})


@app.route('/brand/<int:bid>')
def get_brand_data(bid):
    s = get_session()
    rv = s.query(Data).filter(Data.brand_id == bid).all()
    return jsonify(data_aggregate(rv))


@app.route('/brand/<int:bid>/user')
def get_brand_user_list(bid):
    return jsonify({'users': app.static_data.brand_user.get(bid)})


@app.route('/brand/<int:bid>/user/<int:uid>')
def get_brand_user_data(uid, bid):
    s = get_session()
    rv = s.query(Data).filter(Data.user_id == uid,
                              Data.brand_id == bid).all()
    return jsonify(data_aggregate(rv))


if __name__ == '__main__':
    app.run(debug=True)