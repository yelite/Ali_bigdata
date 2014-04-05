#coding=utf-8

import Causal
import LR
import CF
import Simple
from data import Data
from static import StaticData
from db import s as data_session

models = {'Causal': Causal,
          'LR': LR,
          'CF': CF,
          'Simple': Simple}