from django.conf.urls import *
from portal.views import *
from django.conf.urls import patterns, include, url
from portal import views

urlpatterns = patterns('',
    #Calendar Urls
    url(r'^json/$', CalendarJsonListView.as_view(),name='calendar_json'),
    url(r'^$', CalendarView.as_view(), name='calendar'),
    #Appointment Urls
    url(r'^appointment-form/$', views.appt_form),
    url(r'^make-appointment/$', views.make_appt),
    #Search Urls
    url(r'^search-form/$', views.search_form),
    url(r'^search/$', views.search),

)