from django.urls import path
from .views import (
    register_event, my_events, home, registration_form,
    my_events_form, add_event, todo_list_create, todo_detail,api_login,
)
from django.shortcuts import redirect

urlpatterns = [
    path('', lambda request: redirect('home/', permanent=False)),
    path('home/', home, name='home'),

    # API endpoints
    path('register-event/', register_event, name='register-event'),
    path('my-events/', my_events, name='my-events'),
    path('add-event/', add_event, name='add-event'),
    path('login/', api_login, name='login'),

    # Optional: HTML form pages
    path('register/', registration_form, name='register-form'),
    path('my-events-form/', my_events_form, name='my-events-form'),

    # Todo API endpoints
    path('todos/', todo_list_create, name='todo-list-create'),           # GET to list, POST to create
    path('todos/<int:pk>/', todo_detail, name='todo-detail'),            # GET, PUT, DELETE for a specific todo
]
