#from django.conf.urls import url
from django.urls import include, path

from . import views
        
urlpatterns = [
        ### NOTE: We have switched to the newer and simpler format provided by Django 3.1

        #url(r'^$', views.mainindex, name='mainindex'),
        path('', views.mainindex, name='mainindex'),

        #url(r'^user/(?P<user_id>[0-9]+)/$', views.userindex, name='userindex'),
        path('user/<int:user_id>/', views.userindex, name='userindex'),

        #url(r'^event/(?P<event_id>[0-9]+)/$', views.eventindex, name='eventindex'),
        path('event/<int:event_id>/', views.eventindex, name='eventindex'),

        path('task2/<department>/', views.task2, name='task2'),

        path('task3/<company>/', views.task3, name='task3'),

        path('task4/<int:month>/', views.task4, name='task4'),

        path('task5/', views.task5, name='task5'),
] 
