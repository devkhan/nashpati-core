import functools
from flask import jsonify


def return_json(f):
    @functools.wraps(f)
    def inner(*a, **k):
        return jsonify(f(*a, **k))
    return inner
