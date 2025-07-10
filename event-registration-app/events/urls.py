from django.urls import path
from .views import register_event, my_events, home

urlpatterns = [
    path('', home),
    path('register-event/', register_event, name='register-event'),
    path('my-events/', my_events, name='my-events'),
]
