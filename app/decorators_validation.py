from functools import wraps

from flask import make_response, jsonify
from flask_jwt_extended import verify_jwt_in_request, get_jwt_claims


def adm_required(fn):
    @wraps(fn)
    def wrapper(*args, **kwargs):
        verify_jwt_in_request()
        claims = get_jwt_claims()
        if claims['roles'] == 'admin':
            return fn(*args, **kwargs)
        else:
            return make_response(jsonify(mensagem='não permitido'), 403)

    return wrapper
