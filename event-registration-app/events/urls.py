from django.urls import path
from .views import register_event, my_events, home
from django.shortcuts import redirect

urlpatterns = [
    path('home/', home),
    path('register-event/', register_event, name='register-event'),
    path('my-events/', my_events, name='my-events'),
    path('', lambda request: redirect('home/', permanent=False)),
]
