To develop a user login function with Django REST Framework (DRF), the **easiest and most modern approach** is using **JWT (JSON Web Tokens)** via the `djangorestframework-simplejwt` package. Here's a step-by-step guide:

---

### **Step 1: Install Required Packages**
```bash
pip install djangorestframework djangorestframework-simplejwt
```

---

### **Step 2: Configure `settings.py`**
```python
# settings.py

INSTALLED_APPS = [
    # ...
    'rest_framework',
    'rest_framework_simplejwt',  # Add this
]

REST_FRAMEWORK = {
    'DEFAULT_AUTHENTICATION_CLASSES': [
        'rest_framework_simplejwt.authentication.JWTAuthentication',  # Enable JWT
    ],
}

# Optional: Customize token lifetime (default: 5 mins access, 1 day refresh)
from datetime import timedelta
SIMPLE_JWT = {
    'ACCESS_TOKEN_LIFETIME': timedelta(minutes=15),
    'REFRESH_TOKEN_LIFETIME': timedelta(days=1),
}
```

---

### **Step 3: Add URL Routes for Login/Refresh**
```python
# urls.py (project-level)
from django.urls import path
from rest_framework_simplejwt.views import TokenObtainPairView, TokenRefreshView

urlpatterns = [
    path('api/token/', TokenObtainPairView.as_view(), name='token_obtain_pair'),  # Login
    path('api/token/refresh/', TokenRefreshView.as_view(), name='token_refresh'),  # Refresh token
]
```

---

### **Step 4: Test the Login Endpoint**
Send a **POST request** to `http://localhost:8000/api/token/` with:
```json
{
  "username": "your_username",
  "password": "your_password"
}
```

**Successful Response**:
```json
{
  "access": "eyJhbGciOi... (access token)",
  "refresh": "eyJhbGciOi... (refresh token)"
}
```

---

### **Step 5: Protect API Views**
Use `permission_classes` to restrict access:
```python
# views.py
from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework.permissions import IsAuthenticated

class ProtectedView(APIView):
    permission_classes = [IsAuthenticated]  # Requires valid JWT

    def get(self, request):
        return Response({"message": "Authenticated!"})
```

---

### **Step 6: Include Token in Requests**
Add the token to request headers:
```http
Authorization: Bearer eyJhbGciOi... (access token)
```

---

### **Key Features**
1. **Stateless Authentication**: No server-side sessions.
2. **Security**: Tokens expire automatically.
3. **Simple**: Minimal setup (~15 lines of code).
4. **Built-in Refresh**: Use `/api/token/refresh/` to get new access tokens.

---

### **Full Workflow**
1. User **logs in** → Gets `access` + `refresh` tokens.
2. Use `access` token for **authenticated requests**.
3. When `access` token expires, use `refresh` token to get a new `access` token.

---

### **Why This Approach?**
- ✅ **Industry standard** for modern apps (JWT).
- ✅ No manual token management (handled by `simplejwt`).
- ✅ Scalable and stateless.
- ✅ Built-in token refresh flow.

For basic use cases, this requires **zero custom code**. Extend with user serializers/permissions as needed.