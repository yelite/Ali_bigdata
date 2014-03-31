#coding=utf-8

from sqlalchemy import Column, Integer, Float, Date
from sqlalchemy.ext.declarative import declarative_base
from helper import memoized


Base = declarative_base()


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

    @classmethod
    @memoized
    def get_by_id(cls, session, id):
        return session.query(cls).get(id)







