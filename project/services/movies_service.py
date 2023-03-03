from typing import Optional

from project.dao.base import BaseDAO
from project.exceptions import ItemNotFound
from project.models import Movie


class MovieService:
    def __init__(self, dao: BaseDAO) -> None:
        self.dao = dao

    def get_item(self, pk: int) -> Movie:
        if movie := self.dao.get_by_id(pk):
            return movie
        raise ItemNotFound(f'Genre with pk={pk} not exists.')

    def get_all(self, page: Optional[int] = None, status: Optional[str] = None) -> list[Movie]:
        return self.dao.get_all(page=page, status=status)


    def create(self, movie_data):
        return self.dao.create(movie_data)

    def update(self, movie_data):
        self.dao.update_movie(movie_data)
        return self.dao

    def delete(self, pk):
        self.dao.delete(pk)
