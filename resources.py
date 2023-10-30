from flask import request
from flask_restful import Resource
from auth import authenticate
from flask_jwt_extended import get_jwt_identity
from flask_jwt_extended import jwt_required

import random

class RandomNumberResource(Resource):
    def __init__(self, auth=None):
        self.auth = auth

    @jwt_required()
    def get(self, min_val, max_val):
        current_user = get_jwt_identity()
        token = request.headers.get('Authorization').split('Bearer ')[-1]

        if self.auth is None:
            return {"error": "Auth object is not set."}, 500

        self.auth(token)

        if min_val >= max_val:
            return {"error": "O valor mínimo deve ser menor que o valor máximo."}, 400

        random_number = random.randint(min_val, max_val)
        return {"numero_randomico": random_number, "responsavel": current_user}