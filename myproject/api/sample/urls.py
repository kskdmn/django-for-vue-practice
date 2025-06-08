from django.urls import path

from . import views

urlpatterns = [
    path('sample/', views.SampleListView.as_view()),
    path('sample/<int:pk>/', views.SampleDetailView.as_view()),
]