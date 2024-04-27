from rest_framework.throttling import UserRateThrottle, AnonRateThrottle


class ContactCreateThrottle(UserRateThrottle):
    rate = "10/hour"


class AnonContactCreateThrottle(AnonRateThrottle):
    rate = "5/hour"
