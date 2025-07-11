from rest_framework.decorators import api_view
from rest_framework.response import Response
from rest_framework import status
from .models import Event, Registration
from .serializers import RegistrationSerializer, EventSerializer
from django.http import JsonResponse

def home(request):
    return JsonResponse({"message": "Welcome to the Event Registration"})

@api_view(['POST'])
def register_event(request):
    serializer = RegistrationSerializer(data=request.data)
    if serializer.is_valid():
        serializer.save()
        return Response({"message": "Registration successful!"}, status=status.HTTP_200_OK)
    return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

@api_view(['POst'])
def my_events(request):
    email = request.data.get('email')
    if not email:
        return Response({"error": "Email query parameter is required."}, status=status.HTTP_400_BAD_REQUEST)
    
    registrations = Registration.objects.filter(email=email)
    events = Event.objects.filter(id__in=registrations.values('event'))
    serializer = EventSerializer(events, many=True)
    
    # Format response as per your spec
    response_data = [{"event_id": event['id'], "event_name": event['name']} for event in serializer.data]
    return Response(response_data, status=status.HTTP_200_OK)

