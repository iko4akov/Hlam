from typing import Generic, List, Optional, TypeVar

from flask import current_app
from flask_sqlalchemy import BaseQuery
from sqlalchemy import desc
from sqlalchemy.orm import scoped_session
from werkzeug.exceptions import NotFound
from project.setup.db.models import Base


T = TypeVar('T', bound=Base)

class BaseDAO(Generic[T]):
    __model__ = Base

    def __init__(self, db_session: scoped_session) -> None:
        self._db_session = db_session

    @property
    def _items_per_page(self) -> int:
        return current_app.config['ITEMS_PER_PAGE']

    def get_by_id(self, pk: int) -> Optional[T]:
        return self._db_session.query(self.__model__).get(pk)

    def get_by_email(self, email):
        return self._db_session.query(self.__model__).filter(self.__model__.email == email).first()

    def get_all(self, page: Optional[int] = None, status: Optional[str] = None) -> List[T]:
        stmt: BaseQuery = self._db_session.query(self.__model__)

        if page and status == 'new':
            try:
                if page is not None:
                    stmt = stmt.order_by(desc(self.__model__.year)).limit(12).offset(int(page)-1)
                    return stmt.all()
            except NotFound:
                return '', 404
        if status == 'new':
            try:
                if status is not None:
                    stmt = stmt.order_by(desc(self.__model__.year))
                    return stmt.all()
            except NotFound:
                return '', 404
        if page:
            try:
                if page is not None:
                    stmt = stmt.limit(12).offset(int(page)-1)
                    return stmt.all()
            except NotFound:
                return '', 404

        return stmt.all()

    def create(self, new_data):
        entity = self.__model__(**new_data)
        self._db_session.add(entity)
        self._db_session.commit()
        return entity

    def delete(self, pk):
        object_pk = self._db_session.query(self.__model__).get(pk)
        self._db_session.delete(object_pk)
        self._db_session.commit()

    def update_movie(self, movie_data):
        movie = self.get_by_id(movie_data.get("id"))
        movie.title = movie_data.get("title")
        movie.description = movie_data.get("description")
        movie.trailer = movie_data.get("trailer")
        movie.year = movie_data.get("year")
        movie.rating = movie_data.get("rating")
        movie.genre_id = movie_data.get("genre_id")
        movie.director_id = movie_data.get("director_id")

        self._db_session.add(movie)
        self._db_session.commit()

    def update_dir_and_gen(self, dir_gen_data):
        dir_gen = self.get_by_id(dir_gen_data.get("id"))
        dir_gen.name = dir_gen_data.get("name")

        self._db_session.add(dir_gen)
        self._db_session.commit()


    def update_user(self, user_data):
        user = self.get_by_id(user_data.get("id"))
        user.password = user_data.get("password")

        self._db_session.add(user)
        self._db_session.commit()

    def patch_user(self, user_data):
        user = self.get_by_id(user_data.get("id"))
        if user_data.get("name"):
            user.name = user_data.get("name")
        if user_data.get("surname"):
            user.surname = user_data.get("surname")
        if user_data.get("favorite_genre"):
            user.favorite_genre = user_data.get("favorite_genre")

        self._db_session.add(user)
        self._db_session.commit()

