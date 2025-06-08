from django.urls import path

from . import views

urlpatterns = [
    path('sample/', views.SampleLCView.as_view()),
    path('sample/<int:pk>/', views.SampleRUDView.as_view()),
]