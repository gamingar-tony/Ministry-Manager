from django.contrib.auth.models import User, AbstractUser
from django.db import models
from django.conf import settings

class User(AbstractUser):
    ROLE_CHOICES = [
        ('admin', 'Admin'),
        ('minister', 'Minister'),
        ('volunteer', 'Volunteer'),
    ]

    role = models.CharField(max_length = 10, choices = ROLE_CHOICES, default = 'volunteer')

class ScheduleEntry(models.Model):
    user = models.ForeignKey(User, on_delete = models.CASCADE)
    date = models.DateField()
    time = models.TimeField()
    role = models.CharField(max_length = 100)

    def __str__(self):
        return f"{self.user.username} - {self.role} on {self.date} at {self.time}"

class Schedule(models.Model):
    user = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete = models.CASCADE, null = True, blank = True)
    role = models.CharField(max_length = 100)
    date = models.DateField()
    time = models.TimeField()
    location = models.CharField(max_length = 100, blank = True)

    def __str__(self):
        return f"{self.role} for {self.user.username} on {self.date}"

class Profile(models.Model):
    user = models.OneToOneField(User, on_delete = models.CASCADE, related_name = 'profile')
    email_notifications = models.BooleanField(default = True)
    dark_mode = models.BooleanField(default = False)
    is_superuser = models.BooleanField(default = False)

    def __str__(self):
        return f"{self.user.username}'s Profile"

class Homily(models.Model):
    title = models.CharField(max_length = 200)
    content = models.TextField(blank = True)
    date = models.DateField()
    uploaded_by = models.ForeignKey(User, on_delete = models.SET_NULL, null = True, blank = True)
    file = models.FileField(upload_to = 'homilies/', blank = True, null = True)

    def __str__(self):
        return f"{self.title} ({self.date})"

class Note(models.Model):
    title = models.CharField(max_length = 200)
    content = models.TextField()
    created_by = models.ForeignKey(User, on_delete = models.CASCADE)
    created_at = models.DateTimeField(auto_now_add = True)
    is_public = models.BooleanField(default = False) # Optional: shared note feature

    def __str__(self):
        return self.title