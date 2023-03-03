from flask_restx import Resource, Namespace
from flask import request

from project.container import movie_service
from project.setup.api.models import movie
from project.setup.api.parsers import page_parser, status_parser
from project.helpers.decorators import auth_required

api = Namespace('movies')


@api.route('/')
class MoviesView(Resource):
    # @auth_required
    @api.expect(page_parser)
    @api.expect(status_parser)
    @api.marshal_with(movie, as_list=True, code=200, description='OK')
    def get(self):
        """
        Get movies all
        """
        return movie_service.get_all(**page_parser.parse_args(), **status_parser.parse_args()), 200

    # @admin_required
    def post(self):
        req_json = request.json
        movie = movie_service.create(req_json)
        return "", 201, {"location": f"/movies/{movie.id}"}


@api.route('/<int:movie_id>')
class MovieView(Resource):
    @auth_required
    @api.response(404, 'Not Found')
    @api.marshal_with(movie, as_list=True, code=200, description='OK')
    def get(self, movie_id):
        """
        Get movie by id
        """
        return movie_service.get_item(movie_id), 200

    # @admin_required
    def put(self, movie_id):
        req_json = request.json
        if "id" not in req_json:
            req_json["id"] = movie_id
        movie_service.update(req_json)
        return "", 204

    # @admin_required
    def delete(self, movie_id):
        movie_service.delete(movie_id)
        return "", 204
