#coding=utf-8

from sqlalchemy import Column, Integer, Float, Boolean
from sqlalchemy.ext.declarative import declarative_base

from helper import memoized
from .db import s, engine

Base = declarative_base()


class Customer(Base):
    __tablename__ = 'customer'

    id = Column(Integer, primary_key=True)
    click_purchase = Column(Float, default=0.0)
    idle = Column(Boolean, default=False)
    purchase = Column(Float, default=0.0)


class Brand(Base):
    __tablename__ = 'brand'

    id = Column(Integer, primary_key=True)
    purchase_purchase = Column(Float, default=0.0)
    idle = Column(Boolean, default=False)


def init(session):
    Base.metadata.create_all(engine)
    rv = session.execute('select distinct user_id from data')
    obj = map(lambda x: Customer(id=x[0]), rv.fetchall())
    s.add_all(obj)

    rv = session.execute('select distinct brand_id from data')
    obj = map(lambda x: Brand(id=x[0]), rv.fetchall())
    s.add_all(obj)

    s.commit()

