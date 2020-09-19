from django.shortcuts import render, get_object_or_404

from django.http import HttpResponse, HttpResponseRedirect
from mycalendar.models import User, Event
from django.urls import reverse
import datetime
import operator
from django.utils import timezone

# Create your views here.

def mainindex(request):
        context = { 'user_list': User.objects.all(), 'event_list': Event.objects.all() }
        return render(request, 'mycalendar/index.html', context)

def userindex(request, user_id):
        user = User.objects.get(pk=user_id)
        context = { 'user': user}
        return render(request, 'mycalendar/userindex.html', context)

def eventindex(request, event_id):
        event = Event.objects.get(pk=event_id)
        context = {'event': event}
        return render(request, 'mycalendar/eventindex.html', context)

def task1(request, event_id):
        event = Event.objects.get(pk=event_id)
        context = {'event': event, 'event_duration': (event.end_time - event.start_time).total_seconds()/60}
        return render(request, 'mycalendar/task1.html', context)

def task2(request, department):
        dept_users = [u for u in User.objects.all() if u.department == department]
        context = {'department': department, 'dept_users': dept_users}
        return render(request, 'mycalendar/task2.html', context)

def task3(request, company):
        context = {'company': company, 'company_users': []}
        return render(request, 'mycalendar/task3.html', context)

def task4(request, month):
        context = {'month': month, 'month_events': []}
        return render(request, 'mycalendar/task4.html', context)

def task5(request):
        allevents = Event.objects.all()
        context = {'allevents': allevents}
        return render(request, 'mycalendar/task5.html', context)
