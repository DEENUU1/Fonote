from subscription.services.user_subscription_service import UserSubscriptionService


def mark_expired_user_subscriptions_as_expired() -> bool:
    user_subscription_service = UserSubscriptionService()
    expired_subscriptions = user_subscription_service.get_list_expired_user_subscription()

    for subscription in expired_subscriptions:
        user_subscription_service.update_status("EXPIRED", subscription)

    return True

