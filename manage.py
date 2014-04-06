#coding=utf-8

from db import s
from models import models


def init_model():
    map(lambda x: x.init(s), models.values())


def train_model(name='LR'):
    models[name].train(s)


if __name__ == '__main__':
    train_model()
