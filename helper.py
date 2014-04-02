#coding=utf-8

import os
import collections, functools

root_dic = os.path.split(os.path.realpath(__file__))[0]

def record_aggregate(records, unique_brand=False):
    rv = [0] * 4
    unique_dict = dict()
    for i in records:

        if unique_brand and i.action == 1:
            # only count purchase for unique brands
            if i.brand_id in unique_dict:
                continue
            unique_dict[i.brand_id] = 0

        rv[i.action] += 1
    return rv


class memoized(object):
   '''Decorator. Caches a function's return value each time it is called.
   If called later with the same arguments, the cached value is returned
   (not reevaluated).
   '''
   def __init__(self, func):
      self.func = func
      self.cache = {}
   def __call__(self, *args):
      if not isinstance(args, collections.Hashable):
         # uncacheable. a list, for instance.
         # better to not cache than blow up.
         return self.func(*args)
      if args in self.cache:
         return self.cache[args]
      else:
         value = self.func(*args)
         self.cache[args] = value
         return value
   def __repr__(self):
      '''Return the function's docstring.'''
      return self.func.__doc__
   def __get__(self, obj, objtype):
      '''Support instance methods.'''
      return functools.partial(self.__call__, obj)