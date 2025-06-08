To resolve the issue where `CurrentUserMiddleware.get_current_user()` always returns `None` and make your implementation async-safe, we'll refactor the code to use `contextvars` instead of `threading.local`. Here's a step-by-step explanation and implementation:

### Why `contextvars`?
- **Thread-locals (`threading.local`)** only work in synchronous code and aren't suitable for async environments (like Django ASGI)
- **Context Variables (`contextvars`)** maintain separate state per concurrent task/context, making them safe for both sync and async code

### Updated Implementation

#### 1. `middlewares/current_user.py` (Async-Safe Middleware)
```python
import contextvars
from asgiref.sync import iscoroutinefunction, sync_to_async

# Context variable to store current user
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
```

#### 2. `authentication.py` (JWT Authentication Extension)
```python
from rest_framework_simplejwt.authentication import JWTAuthentication
from .middlewares.current_user import _current_user

class CustomJWTAuthentication(JWTAuthentication):
    def authenticate(self, request):
        result = super().authenticate(request)
        if result:
            user, _ = result
            _current_user.set(user)  # Update context variable
        return result
```

#### 3. `models.py` (Base Model)
```python
from django.contrib.auth import get_user_model
from django.db import models
from middlewares.current_user import CurrentUserMiddleware

User = get_user_model()

class BaseModel(models.Model):
    created_by = models.ForeignKey(
        User, on_delete=models.PROTECT, 
        related_name='%(class)s_created', 
        null=True, blank=True
    )
    created_at = models.DateTimeField(auto_now_add=True)
    updated_by = models.ForeignKey(
        User, on_delete=models.PROTECT,
        related_name='%(class)s_updated',
        null=True, blank=True
    )
    updated_at = models.DateTimeField(auto_now=True)

    class Meta:
        abstract = True

    def save(self, *args, **kwargs):
        current_user = CurrentUserMiddleware.get_current_user()
        
        # Only set if user is authenticated
        if current_user and current_user.is_authenticated:
            if not self.pk and not self.created_by:
                self.created_by = current_user
            self.updated_by = current_user
        
        super().save(*args, **kwargs)
```

### Key Configuration Steps

#### 1. Update Django Settings (`settings.py`)
```python
MIDDLEWARE = [
    # ...
    'django.contrib.auth.middleware.AuthenticationMiddleware',
    'your_app.middlewares.current_user.CurrentUserMiddleware',  # After auth
    # ...
]

REST_FRAMEWORK = {
    'DEFAULT_AUTHENTICATION_CLASSES': (
        'your_app.authentication.CustomJWTAuthentication',  # Custom JWT
        # ...
    )
}
```

#### 2. Migration
Run migrations to apply changes to your models:
```bash
python manage.py makemigrations
python manage.py migrate
```

### How It Works
1. **Middleware Setup**:
   - Sets the current user in a context variable at the start of each request
   - Automatically handles both synchronous and asynchronous requests
   - Cleans up context variable after request completion

2. **JWT Authentication**:
   - Extends SimpleJWT to update the context variable after authentication
   - Ensures DRF views get the authenticated user

3. **Base Model**:
   - Uses `CurrentUserMiddleware.get_current_user()` to access the context variable
   - Automatically sets `created_by` and `updated_by` during save operations
   - Handles both new creations and updates

### Key Benefits
1. **Async Compatibility**: Works with Django's ASGI for async views
2. **DRF Integration**: Properly handles JWT authentication flow
3. **Thread/Context Safety**: Uses context variables instead of thread-locals
4. **Flexible User Handling**: Gracefully handles both authenticated and anonymous users

### Testing Tips
1. Verify middleware order in settings
2. Check that `CustomJWTAuthentication` is used in DRF settings
3. Test with:
   - Authenticated API requests
   - Unauthenticated requests
   - Both sync and async views
   - Admin interface interactions

This implementation ensures that `created_by` and `updated_by` are properly set for all database operations while being compatible with Django's async capabilities and JWT authentication.