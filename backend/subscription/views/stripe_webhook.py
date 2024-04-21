import json

import stripe
from django.conf import settings
from django.http import JsonResponse
from rest_framework.views import APIView

from authentication.services.user_service import UserService
from ..serializers.order_serializer import OrderInputSerializer
from ..serializers.user_subscription_serializer import UserSubscriptionUpdateSerializer
from ..services.order_service import OrderService
from ..services.user_subscription_service import UserSubscriptionService
import logging


logger = logging.getLogger(__name__)
stripe.api_key = settings.STRIPE_SECRET_KEY
webhook_secret = settings.STRIPE_WEBHOOK_SECRET


class Webhook(APIView):
    _user_subscription_service = UserSubscriptionService()
    _order_service = OrderService()
    _user_service = UserService()

    def post(self, request):
        """
            This API handling the webhook .

            :return: returns event details as json response .
        """
        logger.info("Webhook received")

        request_data = json.loads(request.body)
        event = None

        if webhook_secret:
            signature = request.META['HTTP_STRIPE_SIGNATURE']
            try:
                event = stripe.Webhook.construct_event(
                    payload=request.body,
                    sig_header=signature,
                    secret=webhook_secret
                )
                logger.info("Webhook verified")
            except ValueError as err:
                logger.error(f"Error while verifying webhook: {err}")
                raise err
            except stripe.error.SignatureVerificationError as err:
                logger.error(f"Error while verifying webhook: {err}")
                raise err

            event_type = event['type']
        else:
            event_type = request_data['type']

        if event_type == 'checkout.session.completed':
            logger.info("Checkout session completed")
            if event:
                user_id = event.get("data").get("object").get("metadata").get("user_id")
                user_subscription = self._user_subscription_service.get_current_subscription_by_user(int(user_id))

                # Create Order object
                object_data = event.get("data").get("object")
                customer_details_data = object_data.get("customer_details")
                data = {
                    "currency": object_data.get("currency"),
                    "customer": object_data.get("customer"),
                    "city": customer_details_data.get("address").get("city"),
                    "country": customer_details_data.get("address").get("country"),
                    "line1": customer_details_data.get("address").get("line1"),
                    "line2": customer_details_data.get("address").get("line2"),
                    "postal_code": customer_details_data.get("address").get("postal_code"),
                    "state": customer_details_data.get("address").get("state"),
                    "email": customer_details_data.get("email"),
                    "name": customer_details_data.get("name"),
                    "phone": customer_details_data.get("phone"),
                    "total_amount": object_data.get("amount_total"),
                    "invoice_id": object_data.get("invoice"),
                }
                order_serializer = OrderInputSerializer(data=data)
                order_serializer.is_valid(raise_exception=True)
                order = self._order_service.create(order_serializer.validated_data, user_subscription.user)

                # Update UserSubscription object
                user_subscription_update_data = {
                    "status": "ACTIVE",
                    "order": order.pk,
                    "subscription_id": object_data.get("subscription")
                }
                user_subscription_update_serializer = UserSubscriptionUpdateSerializer(
                    data=user_subscription_update_data
                )
                user_subscription_update_serializer.is_valid(raise_exception=True)
                self._user_subscription_service.partial_update(
                    user_subscription.pk,
                    user_subscription_update_serializer.validated_data
                )

        elif event_type == 'invoice.payment_failed':
            logger.info("Invoice payment failed")
            if event:
                # Update UserSubscription object
                user_id = event.get("data").get("object").get("metadata").get("user_id")
                user_subscription = self._user_subscription_service.get_current_subscription_by_user(int(user_id))
                user_subscription_update_data = {
                    "status": "FAILED",
                }
                user_subscription_update_serializer = UserSubscriptionUpdateSerializer(
                    data=user_subscription_update_data
                )
                user_subscription_update_serializer.is_valid(raise_exception=True)
                self._user_subscription_service.partial_update(
                    user_subscription.pk,
                    user_subscription_update_serializer.validated_data
                )
        else:
            pass

        logger.info("Webhook processed")
        return JsonResponse(data={"status": "success"})
