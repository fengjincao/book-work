# -*- coding: utf-8 -*-
from functools import wraps
from flask import jsonify, request
from cerberus import Validator
from bookhouse.models.user import User


def auth_required(f):
    @wraps(f)
    def wrapper(*args, **kwargs):
        token = request.headers.get('Token')
        validator = Validator({
                                'Token': {'type': 'string', 'minlength': 1},
                        })
        if token is None:
            resp_data = {'status': 'fail', 'data': {'message': 'no token', 'code': 0}}
            return jsonify(**resp_data)
        if not validator.validate(token):
            resp_data = {'status': 'fail', 'data': {'message': 'token error', 'code': 1}}
            return jsonify(**resp_data)
        user = User.query.get(int(token))
        if not user:
            resp_data = {'status': 'fail', 'data': {'message': 'user find error', 'code': 2}}
            return jsonify(**resp_data)
        g.user = user
        return f(*args, **kwargs)
    return wrapper
