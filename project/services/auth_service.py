from flask import abort
import datetime
import jwt
import calendar

from project.config import BaseConfig
from project.services.users_service import UserService
from project.tools.security import compare_password


class AuthService:
    def __init__(self, user_service: UserService):
        self.user_service = user_service

    def generate_token(self, email, password, is_refresh=False):
        user = self.user_service.get_by_email(email)

        if user is None:
            raise abort(404)

        if not is_refresh:
            if not compare_password(user.password, password):
                abort(400)

            data = {
                "email": user.email,
                "password": user.password
            }

            min30 = datetime.datetime.utcnow() + datetime.timedelta(minutes=30)
            data["exp"] = calendar.timegm(min30.timetuple())
            access_token = jwt.encode(data, BaseConfig.PWD_HASH_SALT, algorithm=BaseConfig.JWT_ALGO)

            day129 = datetime.datetime.utcnow() + datetime.timedelta(days=129)
            data["exp"] = calendar.timegm(day129.timetuple())
            refresh_token = jwt.encode(data, BaseConfig.PWD_HASH_SALT, algorithm=BaseConfig.JWT_ALGO)

            return {
                "access_token": access_token,
                "refresh_token": refresh_token
            }

    def approve_refresh_token(self, refresh_token):
        data = jwt.decode(jwt=refresh_token, key=BaseConfig.PWD_HASH_SALT, algorithms=[BaseConfig.JWT_ALGO])
        username = data.get("email")

        return self.generate_token(username, None, is_refresh=True)
