from django.urls import path
from . import views

app_name = 'common'

urlpatterns = [
    path('api-logs/', views.APILogListView.as_view(), name='api-logs-list'),
    path('api-logs/<int:pk>/', views.APILogDetailView.as_view(), name='api-logs-detail'),
    path('api-logs/stats/', views.APILogStatsView.as_view(), name='api-logs-stats'),
]
