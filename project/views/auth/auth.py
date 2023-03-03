from flask import request
from flask_restx import Resource, Namespace

from project.container import user_service, auth_service

api = Namespace("auth")

@api.route('/register')
class AuthsView(Resource):

    def post(self):
        """
        Create new user
        """
        req_json = request.json
        user_service.create(req_json)

        return "", 201


@api.route('/login')
class AuthView(Resource):

    def post(self):
        req_json = request.json

        email = req_json.get('email', None)
        password = req_json.get('password', None)
        if None in [email, password]:
            return "", 400

        tokens = auth_service.generate_token(email, password)

        return tokens, 200

    def put(self):
        req_json = request.json
        refresh_token = req_json.get("refresh_token")

        tokens = auth_service.approve_refresh_token(refresh_token)

        return tokens, 200
