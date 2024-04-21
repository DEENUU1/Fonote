from typing import Optional

import stripe
from django.conf import settings
from stripe.checkout import Session

stripe.api_key = settings.STRIPE_SECRET_KEY


class StripeService:

    def cancel_subscription(self, subscription_id: str) -> bool:
        try:
            stripe.Subscription.cancel(subscription_id)
            return True

        except Exception as e:
            # TODO logger
            print(e)
            return False

    def create_checkout_session(self, price_id: str, user_id: int) -> Optional[Session]:
        try:
            checkout_session = stripe.checkout.Session.create(
                line_items=[
                    {
                        'price': price_id,
                        'quantity': 1
                    }
                ],
                metadata={
                    "user_id": user_id
                },
                mode='subscription',
                success_url=settings.FRONTEND_SUBSCRIPTION_SUCCESS_URL + "?session_id={CHECKOUT_SESSION_ID}",
                cancel_url=settings.FRONTEND_SUBSCRIPTION_CANCEL_URL,
            )
            return checkout_session

        except Exception as e:
            # TODO add logger
            print(e)
            return

    def get_invoice(self, invoice_id: str) -> Optional[str]:
        try:
            invoice_data = stripe.Invoice.retrieve(invoice_id)
            return invoice_data.hosted_invoice_url

        except Exception as e:
            # TODO add logger
            print(e)
            return
