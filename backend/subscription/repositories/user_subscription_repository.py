from typing import Dict, Any, Optional, List
from uuid import UUID

from django.contrib.auth.backends import UserModel

from ..models.user_subscription import UserSubscription


class UserSubscriptionRepository:
    """
    Repository for interacting with user subscription data.

    Methods:
        create(data: Dict[str, Any], user: UserModel) -> UserSubscription:
            Creates a new user subscription with the given data and user.

        partial_update(user_subscription: UserSubscription, data: Dict[str, Any]) -> UserSubscription:
            Partially updates a user subscription with the given data.

        user_subscription_exists_by_uuid(_id: UUID) -> bool:
            Checks if a user subscription with the given UUID exists.

        get_user_subscription_by_uuid(_id: UUID) -> UserSubscription:
            Retrieves a user subscription by its UUID.

        get_current_subscription_by_user(user: UserModel) -> Optional[UserSubscription]:
            Retrieves the current subscription for a user, if any.

    Attributes:
        model: The UserSubscription model used for database operations.
    """

    def __init__(self):
        """
        Initialize the UserSubscriptionRepository.
        """
        self.model = UserSubscription

    def create(self, data: Dict[str, Any], user: UserModel) -> UserSubscription:
        """
        Creates a new user subscription with the given data and user.

        Args:
            data (Dict[str, Any]): The data to create the user subscription with.
            user (UserModel): The user associated with the subscription.

        Returns:
            UserSubscription: The created user subscription object.
        """
        return self.model.objects.create(user=user, **data)

    @staticmethod
    def partial_update(user_subscription: UserSubscription, data: Dict[str, Any]) -> UserSubscription:
        """
        Partially updates a user subscription with the given data.

        Args:
            user_subscription (UserSubscription): The user subscription object to update.
            data (Dict[str, Any]): The data to update the user subscription with.

        Returns:
            UserSubscription: The updated user subscription object.
        """
        for key, value in data.items():
            setattr(user_subscription, key, value)
        user_subscription.save()
        return user_subscription

    def user_subscription_exists_by_uuid(self, _id: UUID) -> bool:
        """
        Checks if a user subscription with the given UUID exists.

        Args:
            _id (UUID): The UUID of the user subscription.

        Returns:
            bool: True if the user subscription exists, False otherwise.
        """
        return self.model.objects.filter(id=_id).exists()

    def get_user_subscription_by_uuid(self, _id: UUID) -> UserSubscription:
        """
        Retrieves a user subscription by its UUID.

        Args:
            _id (UUID): The UUID of the user subscription.

        Returns:
            UserSubscription: The user subscription object.
        """
        return self.model.objects.get(id=_id)

    def get_current_subscription_by_user(self, user: UserModel) -> Optional[UserSubscription]:
        """
        Retrieves the current subscription for a user, if any.

        Args:
            user (UserModel): The user.

        Returns:
            Optional[UserSubscription]: The current user subscription, if any.
        """
        return self.model.objects.filter(user=user).first()

    def get_list_user_subscription_status_active(self) -> List[UserSubscription]:
        """
        Retrieves a list of user subscriptions with status "ACTIVE".

        Returns:
            List[UserSubscription]: The list of user subscriptions.
        """
        return self.model.objects.filter(status="ACTIVE")

    @staticmethod
    def update_status(status: str, user_subscription: UserSubscription) -> bool:
        """
        Updates the status of a user subscription.

        Args:
            status (str): The new status.
            user_subscription (UserSubscription): The user subscription to update.
        """
        user_subscription.status = status
        user_subscription.save()
        return True
