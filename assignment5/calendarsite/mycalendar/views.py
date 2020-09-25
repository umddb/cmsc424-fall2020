from django.shortcuts import render, get_object_or_404

from django.http import HttpResponse, HttpResponseRedirect
from mycalendar.models import User, Calendar, Event, BelongsTo
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
        context = {'user': user, 'calendar_list': user.calendar_set.all() }
        return render(request, 'mycalendar/userindex.html', context)

def eventindex(request, event_id):
        event = Event.objects.get(pk=event_id)
        statuses = [(c.title, BelongsTo.Status(BelongsTo.objects.get(event=event, calendar=c).status)) for c in event.calendars.all()]
        context = {'event': event, 'statuses': statuses}
        return render(request, 'mycalendar/eventindex.html', context)

def calendarindex(request, calendar_id):
        context = {'calendar_id': calendar_id, 'event_list': Calendar.objects.get(
            pk=calendar_id).event_set.all().order_by('start_time')}

        for event in context['event_list']:
                print(type(event.start_time))

        date_list = dict()

        for i in range(0, len(context['event_list'])):
                if context['event_list'][i].start_time.strftime("%B %d, %Y") in date_list:
                        date_list[context['event_list'][i].start_time.strftime("%B %d, %Y")].append(context['event_list'][i])
                else:
                        date_list[context['event_list'][i].start_time.strftime("%B %d, %Y")] = [(context['event_list'][i])]

        context['date_list'] = date_list
        return render(request, 'mycalendar/calendarindex.html', context)

############# Create a new event
def createevent(request, user_id):
        context = {'user': User.objects.get(pk=user_id), 'calendar_list': Calendar.objects.all()}
        return render(request, 'mycalendar/createevent.html', context)

def submitcreateevent(request, user_id):
        chosen_calendars = [c for c in Calendar.objects.all() if request.POST["answer{}".format(c.id)] == "true"]
        e = Event(title=request.POST["title"], start_time=request.POST["start_time"], end_time=request.POST["end_time"], created_by = User.objects.get(pk=user_id))
        e.save()
        for c in chosen_calendars:
            bt = BelongsTo(event=e, calendar=c, status=BelongsTo.Status.WAITING_RESPONSE)
            bt.save()
        return HttpResponseRedirect(reverse('createdevent', args=(user_id,e.id,)))

def createdevent(request, user_id, event_id):
    return eventindex(request, event_id)


############# Create a new calendar
def createcalendar(request, user_id):
        context = {'user': User.objects.get(pk=user_id)}
        return render(request, 'mycalendar/createcalendar.html', context)

