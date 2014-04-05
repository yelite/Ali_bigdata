#coding=utf-8

import os
from .model import init
from .predict import Predictor
import test

train = None
package_dic = os.path.split(os.path.realpath(__file__))[0]