from flask_restx import Namespace, Resource
from flask import request

from project.container import director_service
from project.setup.api.models import director
from project.setup.api.parsers import page_parser

api = Namespace('directors')


@api.route('/')
class DirectorsView(Resource):
    # @auth_required
    @api.expect(page_parser)
    @api.marshal_with(director, as_list=True, code=200, description='OK')
    def get(self):
        """
        Get all directors.
        """
        return director_service.get_all(**page_parser.parse_args())

    # @admin_required
    def post(self):
        req_json = request.json
        director = director_service.create(req_json)
        return "", 201, {"location": f"/director/{director.id}"}


@api.route('/<int:director_id>')
class DirectorView(Resource):
    # @auth_required
    @api.response(404, 'Not Found')
    @api.marshal_with(director, code=200, description='OK')
    def get(self, director_id):
        """
        Get director by id
        """
        return director_service.get_item(director_id)

    # @admin_required
    def put(self, did):
        req_json = request.json
        if "id" not in req_json:
            req_json["id"] = did
        director_service.update(req_json)
        return "", 204

    # @admin_required
    def delete(self, did):
        director_service.delete(did)
        return "", 204
