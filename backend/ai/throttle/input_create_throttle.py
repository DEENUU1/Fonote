from rest_framework.throttling import UserRateThrottle


class InputCreateThrottle(UserRateThrottle):
    rate = "5/min"
