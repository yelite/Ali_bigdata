#coding=utf-8


from datetime import date, timedelta

from _db import Session
from models.Trivial.model import Customer, Brand
from models import Data
from helper import record_aggregate


def train():
    # TODO save memory
    brands = session.query(Brand).all()
    map(train_brand, brands)

    customers = session.query(Customer).all()
    map(train_customer, customers)

    session.commit()


if __name__ == "__main__":
    train()
