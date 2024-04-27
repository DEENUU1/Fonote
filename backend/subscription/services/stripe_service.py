import logging
from typing import Optional
from uuid import UUID

import stripe
from django.conf import settings
from rest_framework.exceptions import APIException, NotFound
from stripe.checkout import Session

logger = logging.getLogger(__name__)


class StripeService:
    """
    Service class for interacting with the Stripe API.

    Attributes:
        None

    Methods:
        cancel_subscription(subscription_id: str) -> bool:
            Cancels a subscription on Stripe.

        create_checkout_session(price_id: str, user_id: int, plan_id: UUID) -> Optional[Session]:
            Creates a checkout session for subscribing to a plan.

        get_invoice(invoice_id: str) -> Optional[str]:
            Retrieves the hosted invoice URL for a specific invoice.
    """

    def __init__(self):
        """
        Initializes the StripeService with the Stripe secret key from Django settings.
        """
        if not settings.STRIPE_SECRET_KEY:
            logger.error("Stripe secret key not found in settings")

        stripe.api_key = settings.STRIPE_SECRET_KEY

    @staticmethod
    def cancel_subscription(subscription_id: str) -> bool:
        """
        Cancels a subscription on Stripe.

        Args:
            subscription_id (str): The ID of the subscription to cancel.

        Returns:
            bool: True if the cancellation was successful, False otherwise.
        """
        try:
            stripe.Subscription.cancel(subscription_id)
            logger.info(f"Subscription {subscription_id} canceled")
            return True

        except Exception as e:
            logger.error(f"Error while canceling subscription {subscription_id}: {e}")
            return False

    @staticmethod
    def create_checkout_session(price_id: str, user_id: int, plan_id: UUID) -> Optional[Session]:
        """
        Creates a checkout session for subscribing to a plan.

        Args:
            price_id (str): The ID of the price associated with the plan.
            user_id (int): The ID of the user initiating the checkout.
            plan_id (UUID): The ID of the plan being subscribed to.

        Returns:
            Optional[Session]: The created checkout session, or None if creation fails.
        """
        try:
            checkout_session = stripe.checkout.Session.create(
                line_items=[
                    {
                        'price': price_id,
                        'quantity': 1
                    }
                ],
                metadata={
                    "user_id": user_id,
                    "plan_id": plan_id
                },
                mode='subscription',
                success_url=settings.FRONTEND_SUBSCRIPTION_SUCCESS_URL + "?session_id={CHECKOUT_SESSION_ID}",
                cancel_url=settings.FRONTEND_SUBSCRIPTION_CANCEL_URL,
            )
            return checkout_session

        except Exception as e:
            logger.error(f"Error while creating checkout session: {e}")
            raise APIException(detail="Error creating checkout session :(")

    @staticmethod
    def get_invoice(invoice_id: str) -> Optional[str]:
        """
        Retrieves the hosted invoice URL for a specific invoice.

        Args:
            invoice_id (str): The ID of the invoice.

        Returns:
            Optional[str]: The URL of the hosted invoice, or None if retrieval fails.
        """
        try:
            invoice_data = stripe.Invoice.retrieve(invoice_id)
            logger.info(f"Retrieved invoice {invoice_id}")
            return invoice_data.hosted_invoice_url

        except Exception as e:
            logger.error(f"Error while retrieving invoice: {e}")
            raise NotFound(detail="Invoice not found!")
