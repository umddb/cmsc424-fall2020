from django.db import models
from django.utils.translation import gettext_lazy as _

# Create your models here.
import datetime
from django.utils import timezone

class User(models.Model):
        name = models.CharField(max_length=50)
        department = models.CharField(max_length=50)
        company = models.CharField(max_length=50)
        def __str__(self):
                return self.name

class Event(models.Model):
        title = models.CharField(max_length=50)
        start_time = models.DateTimeField()
        end_time = models.DateTimeField()
        def __str__(self):
                return self.title
