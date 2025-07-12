from django.urls import path
from .views import register_event, my_events, home, registration_form, my_events_form, add_event
from django.shortcuts import redirect

urlpatterns = [
    path('', lambda request: redirect('home/', permanent=False)),
    path('home/', home, name='home'),

    # API endpoints
    path('register-event/', register_event, name='register-event'),
    path('my-events/', my_events, name='my-events'),
    path('add-event/', add_event, name='add-event'),

    # Optional: HTML form pages (if you created them)
    path('register/', registration_form, name='register-form'),
    path('my-events-form/', my_events_form, name='my-events-form'),
]


