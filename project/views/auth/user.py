from flask import request
from flask_restx import Resource, Namespace

from project.container import user_service
from project.setup.api.models import user
from project.helpers.decorators import auth_required
api = Namespace('user')


@api.route('/')

class UsersView(Resource):

    @api.marshal_with(user, code=200, as_list=True, description='OK')
    def get(self):
        return user_service.get_all(), 200


@api.route('/<int:uid>')
class UserView(Resource):
    @api.response(404, 'Not Found')
    @api.marshal_with(user, code=200, description='OK')
    def get(self, uid):
        return user_service.get_item(uid), 200


    @auth_required
    def patch(self, uid):
        """
        Edited only name, surname, favorite_genre
        """
        req_json = request.json
        if "id" not in req_json:
            req_json["id"] = uid
        return user_service.patch_user(req_json)

    # @admin_required
    def delete(self, uid):
        user_service.delete(uid)
        return "", 204

@api.route('/password')
class User_pas_View(Resource):
    @auth_required
    def put(self):
        """
        Edite only password
        """
        req_json = request.json

        return user_service.update(req_json)
