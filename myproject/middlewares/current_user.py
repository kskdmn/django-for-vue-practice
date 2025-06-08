import threading

_local = threading.local()


class CurrentUserMiddleware:
    """
    Middleware to store the current user in a thread-local storage.
    This allows access to the current user in any part of the application
    without passing it explicitly.
    """

    def __init__(self, get_response):
        self.get_response = get_response

    def __call__(self, request):
        _local.current_user = getattr(request, 'user', None)
        response = self.get_response(request)
        _local.current_user = None  # Clear after response
        return response

    @staticmethod
    def get_current_user():
        return getattr(_local, 'current_user', None)