#coding=utf-8
__author__ = 'Yelite'

from flask.json import JSONEncoder as _JSONEncoder


class JSONEncoder(_JSONEncoder):
    def default(self, o):
        try:
            iterable = iter(o)
        except TypeError:
            pass
        else:
            return list(iterable)
        return super(JSONEncoder, self).default(o)


def json_patch(app):
    app.json_encoder = JSONEncoder
    return app