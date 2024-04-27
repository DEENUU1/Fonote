from django.contrib.auth.backends import UserModel
from rest_framework.exceptions import NotFound

from ..repositories.user_repository import UserRepository


class UserService:
    """
    Service for handling user-related operations.

    Attributes:
        user_repository: An instance of UserRepository for interacting with user data.

    Methods:
        get_user_by_id(user_id: int) -> UserModel:
            Retrieves a user by their ID.

    Raises:
        NotFound: If the user with the given ID does not exist.
    """

    def __init__(self):
        """
        Initialize the UserService.
        """
        self.user_repository = UserRepository()

    def get_user_by_id(self, user_id: int) -> UserModel:
        """
        Retrieves a user by their ID.

        Args:
            user_id (int): The ID of the user to retrieve.

        Returns:
            UserModel: The user object.

        Raises:
            NotFound: If the user with the given ID does not exist.
        """
        if not self.user_repository.user_exists_by_id(user_id):
            raise NotFound

        return self.user_repository.get_user_by_id(user_id)
