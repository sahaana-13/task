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
@api_view(['POST'])
def my_events(request):
    email = request.data.get('email')
    if not email:
        return Response({"error": "Email query parameter is required."}, status=status.HTTP_400_BAD_REQUEST)
    
    registrations = Registration.objects.filter(email=email)
    events = Event.objects.filter(id__in=registrations.values('event'))
    serializer = EventSerializer(events, many=True)
    
    response_data = [
        {"event_id": event["id"], "event_name": event["name"]}
        for event in serializer.data
    ]
    return Response(response_data, status=status.HTTP_200_OK)
