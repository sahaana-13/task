from django.db import models
from django.contrib.auth.models import User  # Import the built-in User model

# Event Model
class Event(models.Model):
    name = models.CharField(max_length=255)

    def __str__(self):
        return self.name

# Registration Model linked to User
class Registration(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE, null=True, blank=True)  # Link to the authenticated user
    event = models.ForeignKey(Event, on_delete=models.CASCADE)
    name = models.CharField(max_length=255)
    college = models.CharField(max_length=255)
    email = models.EmailField()

    def __str__(self):
        return f"{self.name} ({self.email}) - {self.event.name}"

# Todo Model
class Todo(models.Model):
    title = models.CharField(max_length=255)
    description = models.TextField(blank=True)
    completed = models.BooleanField(default=False)
    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return self.title
