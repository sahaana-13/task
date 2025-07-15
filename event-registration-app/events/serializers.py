from rest_framework import serializers
from .models import Event, Registration, Todo
from django.contrib.auth.models import User

# Event Serializer
class EventSerializer(serializers.ModelSerializer):
    class Meta:
        model = Event
        fields = ['id', 'name']

# Todo Serializer
class TodoSerializer(serializers.ModelSerializer):
    class Meta:
        model = Todo
        fields = '__all__'

# Registration Serializer with user field
class RegistrationSerializer(serializers.ModelSerializer):
    user = serializers.PrimaryKeyRelatedField(queryset=User.objects.all())  # expect user ID

    class Meta:
        model = Registration
        fields = ['event', 'name', 'college', 'email', 'user']
