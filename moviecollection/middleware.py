import logging
from django.core.cache import cache

logger = logging.getLogger(__name__)


class RequestCountMiddleware:
    def __init__(self, get_response):

        self.get_response = get_response
        # One-time configuration and initialization.

    def __call__(self, request):

        # Code to be executed for each request before
        # the view (and later middleware) are called.

        # getting the current count
        current_count = cache.get("request_count", 0)

        # setting the updated count
        cache.set("request_count", current_count + 1)
        response = self.get_response(request)

        # Code to be executed for each request/response after
        # the view is called.

        return response
