#coding=utf-8

import os
from .model import init
# from .train import train
from .predict import Predictor
import test

package_dic = os.path.split(os.path.realpath(__file__))[0]