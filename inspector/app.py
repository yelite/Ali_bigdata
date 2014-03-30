#coding=utf-8

from flask import Flask, abort
from db import Session
from model import Brand, Customer

app = Flask(__name__)

app.route('/purchase/brand/<id>')
def brand_pur_info(id):
    s = Session()
    b = s.query(Brand).get(id)
    if not b:
        abort(404)

    pass
