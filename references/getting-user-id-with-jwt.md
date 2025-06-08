To resolve the issue where `CurrentUserMiddleware.get_current_user()` always returns `None`, you need to ensure the middleware runs **after** authentication middleware and that the thread-local user is set correctly for DRF views using JWT authentication. Here's the step-by-step solution:

### 1. Fix Middleware Order
Ensure `CurrentUserMiddleware` runs after Django's `AuthenticationMiddleware` in `settings.py`:
```python
MIDDLEWARE = [
    # ...
    'django.contrib.auth.middleware.AuthenticationMiddleware',
    # ...
    'your_app.middleware.CurrentUserMiddleware',  # After auth middleware
]
```

### 2. Add Helper Function for User-Setting
Update `current_user.py` with a `set_current_user()` function:
```python
import threading

_local = threading.local()

def set_current_user(user):
    _local.current_user = user

class CurrentUserMiddleware:
    def __init__(self, get_response):
        self.get_response = get_response

    def __call__(self, request):
        set_current_user(request.user)  # Set initial user
        response = self.get_response(request)
        set_current_user(None)  # Clear after response
        return response

    @staticmethod
    def get_current_user():
        return getattr(_local, 'current_user', None)
```

### 3. Create Custom JWT Authentication
Override JWT authentication to update the thread-local user after successful authentication:
```python
# authentication.py
from rest_framework_simplejwt.authentication import JWTAuthentication
from your_app.middleware.current_user import set_current_user

class CustomJWTAuthentication(JWTAuthentication):
    def authenticate(self, request):
        result = super().authenticate(request)
        if result is not None:
            user, _ = result
            set_current_user(user)  # Update to JWT user
        return result
```

### 4. Configure DRF to Use Custom Authentication
Update `settings.py` to use your custom authentication class:
```python
REST_FRAMEWORK = {
    'DEFAULT_AUTHENTICATION_CLASSES': (
        'your_app.authentication.CustomJWTAuthentication',  # Use custom class
        # ... other classes if needed
    )
}
```

### Key Fixes Explained:
1. **Middleware Order**: Ensures `request.user` is populated by Django's auth middleware before your middleware runs.
2. **DRF JWT Handling**: DRF's authentication happens **after** middleware. The custom authentication class updates the thread-local user to the JWT-authenticated user.
3. **Thread-Local Management**: 
   - Middleware sets an initial user (from session/auth)
   - Custom JWT auth overrides it with the JWT user
   - User is cleared post-request to avoid leaks

### Additional Notes:
- **Non-DRF Views**: Works automatically since `request.user` is set by Django's auth.
- **Async Safety**: This solution uses thread-locals, so it's not async-compatible. For async, use contextvars instead.
- **Model Save**: Your `BaseModel.save()` will now correctly get the authenticated user from the thread-local storage.

This approach ensures that both session-based (non-DRF) and JWT-based (DRF) authentications correctly populate `created_by` and `updated_by` fields.