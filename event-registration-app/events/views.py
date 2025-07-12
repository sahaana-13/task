from rest_framework.decorators import api_view
from rest_framework.response import Response
from rest_framework import status
from .models import Event, Registration
from .serializers import RegistrationSerializer, EventSerializer
from django.shortcuts import render

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
    
# API endpoint: POST /my-events/
@api_view(['GET'])
def my_events(request):
    email = request.query_params.get('email')
    if not email:
        return Response({"error": "Email query parameter is required."}, status=status.HTTP_400_BAD_REQUEST)

    # Get all registrations for that email
    registrations = Registration.objects.filter(email=email)

    # Get event IDs from those registrations
    event_ids = registrations.values_list('event_id', flat=True)

    # Fetch event objects for those IDs
    events = Event.objects.filter(id__in=event_ids)

    # Serialize event queryset
    serializer = EventSerializer(events, many=True)

    # Map serializer data to your expected JSON format
    response_data = [
        {"event_id": event["id"], "event_name": event["name"]}
        for event in serializer.data
    ]

    return Response(response_data, status=status.HTTP_200_OK)

@api_view(['POST'])
def add_event(request):
    name = request.data.get('name')

    if not name:
        return Response(
            {"error": "Event name is required."},
            status=status.HTTP_400_BAD_REQUEST
        )

    # Create the event
    event = Event.objects.create(name=name)
    
    return Response(
        {"message": "Event created successfully!", "event_id": event.id, "event_name": event.name},
        status=status.HTTP_201_CREATED
    )

# views.py

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

@api_view(['GET', 'PUT', 'DELETE'])
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
    elif request.method == 'DELETE':
        todo.delete()
        return Response(status=status.HTTP_204_NO_CONTENT)

