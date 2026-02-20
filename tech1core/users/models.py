from django.db import models
from django.contrib.auth.models import AbstractUser
# Create your models here.


class User(AbstractUser):
    ROLE_CHOICES = (
        ("ADMIN", "Admin"),
        ("SUPERVISOR", "Supervisor"),
        ("TECHNICIAN", "Technician"),
        ("VIEWER", "Viewer"),

    )
    role = models.CharField(max_length=20, choices=ROLE_CHOICES)