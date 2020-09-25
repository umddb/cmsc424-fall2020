from django.conf.urls import url

from . import views
        
urlpatterns = [
        url(r'^$', views.mainindex, name='mainindex'),

        url(r'^user/(?P<user_id>[0-9]+)/$', views.userindex, name='userindex'),

        url(r'^event/(?P<event_id>[0-9]+)/$', views.eventindex, name='eventindex'),

        url(r'^calendar/(?P<calendar_id>[0-9]+)/$', views.calendarindex, name='calendarindex'),

        url(r'^user/(?P<user_id>[0-9]+)/createevent$', views.createevent, name='createevent'),

        url(r'^user/(?P<user_id>[0-9]+)/submitcreateevent/$', views.submitcreateevent, name='submitcreateevent'),

        url(r'^user/(?P<user_id>[0-9]+)/createdevent/(?P<event_id>[0-9]+)/$', views.createdevent, name='createdevent'),

        url(r'^user/(?P<user_id>[0-9]+)/createcalendar$', views.createcalendar, name='createcalendar'),
] 
