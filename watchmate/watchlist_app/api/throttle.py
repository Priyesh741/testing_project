from rest_framework.throttling import UserRateThrottle

class ReviewCreatethrottle(UserRateThrottle):
    scope='ReviewCreate'

class ReviewListthrottle(UserRateThrottle):
    scope='ReviewList'