import logging
from typing import Optional
from uuid import UUID

import stripe
from django.conf import settings
from rest_framework.exceptions import APIException, NotFound
from stripe.checkout import Session

logger = logging.getLogger(__name__)
stripe.api_key = settings.STRIPE_SECRET_KEY


class StripeService:

    def cancel_subscription(self, subscription_id: str) -> bool:
        try:
            stripe.Subscription.cancel(subscription_id)
            logger.info(f"Subscription {subscription_id} canceled")
            return True

        except Exception as e:
            logger.error(f"Error while canceling subscription {subscription_id}: {e}")
            return False

    def create_checkout_session(self, price_id: str, user_id: int, plan_id: UUID) -> Optional[Session]:
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
            raise APIException(detail="Error creating checkout session")

    def get_invoice(self, invoice_id: str) -> Optional[str]:
        try:
            invoice_data = stripe.Invoice.retrieve(invoice_id)
            logger.info(f"Retrieved invoice {invoice_id}")
            return invoice_data.hosted_invoice_url

        except Exception as e:
            logger.error(f"Error while retrieving invoice: {e}")
            raise NotFound(detail="Invoice not found")
