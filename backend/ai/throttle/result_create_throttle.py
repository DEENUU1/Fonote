from rest_framework.throttling import UserRateThrottle


class ResultCreateThrottle(UserRateThrottle):
    rate = "10/min"
