from django.core.management.base import BaseCommand

from subscription.tasks import mark_expired_user_subscriptions_as_expired


class Command(BaseCommand):
    help = "Change status of expired subscriptions"

    def handle(self, *args, **options):
        marked_subscriptions = mark_expired_user_subscriptions_as_expired()

        if not marked_subscriptions:
            self.stdout.write(
                self.style.ERROR("Error while trying to mark expired subscriptions")
            )
            return

        self.stdout.write(
            self.style.SUCCESS(
                "Successfully marked expired subscriptions"
            )
        )
