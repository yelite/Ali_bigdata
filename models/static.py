#coding=utf-8


from helper import root_dic
import os


class StaticData:
    def __init__(self, test=False):
        data_dir = 'tests/data' if test else 'data'
        name = 'user_brand.txt'
        path = os.path.join(root_dic,
                            data_dir,
                            name)
        self.user_brand = self.init_user_brand(path)

    @staticmethod
    def init_user_brand(path):
        f = open(path)
        rv = {}
        count = 0
        for l in f:
            name, brands = l.split('\t')
            brands = brands.strip()
            if not brands:
                rv[int(name)] = set()
                continue
            brands = map(int, brands.split(','))
            count += len(brands)
            rv[int(name)] = set(brands)
        f.close()
        return rv