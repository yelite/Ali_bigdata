#coding=utf-8

import Causal
import LR
import CF
import Simple
from data import Data
from static import StaticData
import RandomForest
import SVM

models = {'Causal': Causal,
          'LR': LR,
          'CF': CF,
          'Simple': Simple,
          'RandomForest': RandomForest,
          'SVM': SVM}