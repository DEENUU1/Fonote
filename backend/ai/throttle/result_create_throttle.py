from rest_framework.throttling import UserRateThrottle


class ResultCreateThrottle(UserRateThrottle):
    rate = "5/min"
