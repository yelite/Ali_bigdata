#coding=utf-8


from _db import s
from models.LR.train import DataTrainer


def train():
    t = DataTrainer(s, test=True)
    t.train()
    t.freeze()


if __name__ == "__main__":
    train()
