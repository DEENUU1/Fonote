from rest_framework.throttling import UserRateThrottle


class ResultCreateThrottle(UserRateThrottle):
    rate = "60/min"
