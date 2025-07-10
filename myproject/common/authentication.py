from rest_framework_simplejwt.authentication import JWTAuthentication
from middlewares.current_user import _current_user


class CustomJWTAuthentication(JWTAuthentication):
    """
    Custom JWT Authentication that updates the current user context variable.
    """
    def authenticate(self, request):
        result = super().authenticate(request)
        if result:
            user, _ = result
            _current_user.set(user)  # Update context variable
        return result
