from rest_framework.decorators import api_view
from rest_framework.response import Response
from rest_framework import status
from django.shortcuts import render, redirect
from django.contrib.auth import authenticate, login
from django.contrib import messages
from .models import Event, Registration, Todo
from .serializers import RegistrationSerializer, EventSerializer, TodoSerializer
from django.contrib.auth import login

# Homepage view - renders home.html
def home(request):
    events = Event.objects.all()
    return render(request, 'home.html')

# Registration form page (optional)
def registration_form(request):
    return render(request, 'register.html')

# My events form page (optional)
def my_events_form(request):
    return render(request, 'my_events.html')

# API endpoint: POST /register-event/
@api_view(['POST'])
def register_event(request):
    event_id = request.data.get('event')
    email = request.data.get('email')

    if not event_id or not email:
        return Response(
            {"error": "Both event and email are required."},
            status=status.HTTP_400_BAD_REQUEST
        )
    
    # Check for duplicate registration
    if Registration.objects.filter(event_id=event_id, email=email).exists():
        return Response(
            {"message": "You have already registered for this event."},
            status=status.HTTP_200_OK
        )

    serializer = RegistrationSerializer(data=request.data)
    if serializer.is_valid():
        serializer.save()
        return Response({"message": "Registration successful!"}, status=status.HTTP_200_OK)
    return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

# API endpoint: GET /my-events/
@api_view(['GET'])
def my_events(request):
    email = request.query_params.get('email')
    if not email:
        return Response({"error": "Email query parameter is required."}, status=status.HTTP_400_BAD_REQUEST)

    registrations = Registration.objects.filter(email=email)
    event_ids = registrations.values_list('event_id', flat=True)
    events = Event.objects.filter(id__in=event_ids)
    serializer = EventSerializer(events, many=True)
    response_data = [
        {"event_id": event["id"], "event_name": event["name"]}
        for event in serializer.data
    ]
    return Response(response_data, status=status.HTTP_200_OK)

# API endpoint: POST /add-event/
@api_view(['POST'])
def add_event(request):
    name = request.data.get('name')
    if not name:
        return Response({"error": "Event name is required."}, status=status.HTTP_400_BAD_REQUEST)

    event = Event.objects.create(name=name)
    return Response({
        "message": "Event created successfully!",
        "event_id": event.id,
        "event_name": event.name
    }, status=status.HTTP_201_CREATED)

# API endpoint: GET, POST /todos/
@api_view(['GET', 'POST'])
def todo_list_create(request):
    if request.method == 'GET':
        todos = Todo.objects.all()
        serializer = TodoSerializer(todos, many=True)
        return Response(serializer.data)
    
    elif request.method == 'POST':
        serializer = TodoSerializer(data=request.data)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data, status=status.HTTP_201_CREATED)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

# API endpoint: GET, PUT, PATCH, DELETE /todos/<int:pk>/
@api_view(['GET', 'PUT', 'PATCH', 'DELETE'])
def todo_detail(request, pk):
    try:
        todo = Todo.objects.get(pk=pk)
    except Todo.DoesNotExist:
        return Response({"error": "Todo not found."}, status=status.HTTP_404_NOT_FOUND)

    if request.method == 'GET':
        serializer = TodoSerializer(todo)
        return Response(serializer.data)
    
    elif request.method == 'PUT':
        serializer = TodoSerializer(todo, data=request.data)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
    
    elif request.method == 'PATCH':
        serializer = TodoSerializer(todo, data=request.data, partial=True)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

    elif request.method == 'DELETE':
        todo.delete()
        return Response(status=status.HTTP_204_NO_CONTENT)

# API endpoint: POST /api/login/
@api_view(['POST'])
def api_login(request):
    username = request.data.get('username')
    password = request.data.get('password')

    if not username or not password:
        return Response({"error": "Username and password required."}, status=status.HTTP_400_BAD_REQUEST)

    user = authenticate(request, username=username, password=password)
    if user is not None:
        login(request, user)
        # You can extend this to return tokens if needed
        return Response({
            "message": "Login successful!",
            "username": user.username,
            "email": user.email,
        })
    else:
        return Response({"error": "Invalid credentials."}, status=status.HTTP_401_UNAUTHORIZED)
