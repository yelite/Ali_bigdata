#coding=utf-8

import os
import collections
import functools


root_dic = os.path.split(os.path.realpath(__file__))[0]


def record_aggregate(records, unique_brand=False, unique_date=False):
    rv = [0] * 4
    unique_dict = dict()
    for i in records:

        if unique_brand and i.action == 1:
            # only count purchase for unique brands
            if i.brand_id in unique_dict:
                continue
            unique_dict[i.brand_id] = 0

        if unique_date and i.action == 1:
            if i.time in unique_dict:
                continue
            unique_dict[i.time] = 0

        rv[i.action] += 1
    return rv