from django.urls import path

from . import views

urlpatterns = [
    path('sample/', views.SampleLCView.as_view()),
    path('sample/<int:pk>/', views.SampleRUDView.as_view()),
    path('hello/', views.hello, name='hello'),
    path('say-hello/', views.say_hello, name='say_hello'),
    path('say-test/', views.say_test, name='say_test'),
    path('say-hi/', views.say_hi, name='say_hi'),
    path('increment/<int:number>/', views.increment, name='increment'),
]