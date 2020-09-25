from django.db import models
from django.utils.translation import gettext_lazy as _

# Create your models here.
import datetime
from django.utils import timezone

class User(models.Model):
        name = models.CharField(max_length=50)
        def __str__(self):
                return self.name

class Calendar(models.Model):
        title = models.CharField(max_length=50)
        owner = models.ForeignKey(User, on_delete=models.CASCADE)
        description = models.CharField(max_length=500)
        def __str__(self):
                return self.title

class Event(models.Model):
        title = models.CharField(max_length=50)
        start_time = models.DateTimeField()
        end_time = models.DateTimeField()
        calendars = models.ManyToManyField(Calendar, through='BelongsTo')
        created_by = models.ForeignKey(User, on_delete=models.CASCADE)
        def __str__(self):
                return self.title

class BelongsTo(models.Model):
    class Status(models.TextChoices):
        ACCEPTED = 'AC', _('Accepted')
        DECLINED = 'DE', _('Declined')
        TENTATIVE = 'TE', _('Tentative')
        WAITING_RESPONSE = 'WR', _('Waiting Response')

    event = models.ForeignKey(Event, on_delete=models.CASCADE)
    calendar = models.ForeignKey(Calendar, on_delete=models.CASCADE)
    status = models.CharField(max_length=2, choices=Status.choices, default=Status.WAITING_RESPONSE)
    def __str__(self):
            return "{} in {}: {}".format(self.event, self.calendar, self.status)
