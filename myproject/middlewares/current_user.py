import contextvars
from asgiref.sync import iscoroutinefunction

_current_user = contextvars.ContextVar("current_user", default=None)

class CurrentUserMiddleware:

    def __init__(self, get_response):
        self.get_response = get_response
        self._is_async = iscoroutinefunction(get_response)

    def __call__(self, request):
        if self._is_async:
            return self._async_call(request)
        return self._sync_call(request)

    def _sync_call(self, request):
        # Set context var for sync requests
        token = _current_user.set(request.user)
        try:
            return self.get_response(request)
        finally:
            _current_user.reset(token)

    async def _async_call(self, request):
        # Set context var for async requests
        token = _current_user.set(request.user)
        try:
            return await self.get_response(request)
        finally:
            _current_user.reset(token)

    @staticmethod
    def get_current_user():
        return _current_user.get()