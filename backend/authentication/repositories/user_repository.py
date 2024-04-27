from django.contrib.auth.backends import UserModel


class UserRepository:
    """
    Repository for interacting with user data.

    Methods:
        get_user_by_id(user_id: int) -> UserModel:
            Retrieves a user by their ID.

        user_exists_by_id(user_id: int) -> bool:
            Checks if a user with the given ID exists.
    """

    def __init__(self):
        """
        Initialize the UserRepository.
        """
        self.model = UserModel

    def get_user_by_id(self, user_id: int) -> UserModel:
        """
        Retrieves a user by their ID.

        Args:
            user_id (int): The ID of the user.

        Returns:
            UserModel: The user object.
        """
        return self.model.objects.get(id=user_id)

    def user_exists_by_id(self, user_id: int) -> bool:
        """
        Checks if a user with the given ID exists.

        Args:
            user_id (int): The ID of the user.

        Returns:
            bool: True if the user exists, False otherwise.
        """
        return self.model.objects.filter(id=user_id).exists()
