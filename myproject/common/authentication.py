# authentication.py
from rest_framework_simplejwt.authentication import JWTAuthentication
from middlewares.current_user import CurrentUserMiddleware

class CustomJWTAuthentication(JWTAuthentication):
    def authenticate(self, request):
        result = super().authenticate(request)
        if result is not None:
            user, _ = result
            CurrentUserMiddleware.set_current_user(user)  # Update to JWT user
        return result