from django.urls import path
from rest_framework_simplejwt.views import TokenObtainPairView, TokenRefreshView

urlpatterns = [
    path('', TokenObtainPairView.as_view(), name='token_obtain_pair'),  # Login
    path('refresh/', TokenRefreshView.as_view(), name='token_refresh'),  # Refresh token
]