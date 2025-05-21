from django.contrib.auth.models import AbstractUser
from django.db import models

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