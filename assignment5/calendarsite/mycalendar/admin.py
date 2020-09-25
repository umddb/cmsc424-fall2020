from django.contrib import admin
from mycalendar.models import User, Event, Calendar

# Register your models here.
admin.site.register(User)
admin.site.register(Event)
admin.site.register(Calendar)
