from django.contrib.auth.backends import UserModel


class UserRepository:
    def __init__(self):
        self.model = UserModel

    def get_user_by_id(self, user_id: int) -> UserModel:
        return self.model.objects.get(id=user_id)

    def user_exists_by_id(self, user_id: int) -> bool:
        return self.model.objects.filter(id=user_id).exists()
