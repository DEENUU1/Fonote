from rest_framework.throttling import UserRateThrottle


class InputCreateThrottle(UserRateThrottle):
    rate = "10/min"
