#coding=utf-8

from datetime import datetime
import logging

from sqlalchemy import Column, Integer, Float, Date
from sqlalchemy.ext.declarative import declarative_base


Base = declarative_base()


class Data(Base):
    __tablename__ = 'data'

    id = Column(Integer, primary_key=True)
    user_id = Column(Integer, index=True, nullable=False)
    brand_id = Column(Integer, index=True, nullable=False)
    time = Column(Date, index=True, nullable=False)
    action = Column(Integer, nullable=False)

    __mapper_args__ = {'order_by': id.desc()}


class Customer(Base):
    __tablename__ = 'customer'

    id = Column(Integer, primary_key=True)
    click_purchase = Column(Float, default=0.0)
    save_purchase = Column(Float, default=0.0)
    cart_purchase = Column(Float, default=0.0)
    purchase = Column(Float, default=0.0)


class Brand(Base):
    __tablename__ = 'brand'

    id = Column(Integer, primary_key=True)
    click_purchase = Column(Float, default=0.0)
    purchase_purchase = Column(Float, default=0.0)
    cart_purchase = Column(Float, default=0.0)






