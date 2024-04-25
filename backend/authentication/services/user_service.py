from ..repositories.user_repository import UserRepository
from django.contrib.auth.backends import UserModel
from typing import Optional
from rest_framework.exceptions import NotFound


class UserService:
    def __init__(self):
        self.user_repository = UserRepository()

    def get_user_by_id(self, user_id: int) -> UserModel:
        if not self.user_repository.user_exists_by_id(user_id):
            raise NotFound

        return self.user_repository.get_user_by_id(user_id)

