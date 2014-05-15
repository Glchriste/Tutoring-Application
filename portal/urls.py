from django.conf.urls import *
from portal.views import *
from django.conf.urls import patterns, include, url

urlpatterns = patterns('',

    # Main web portal entrance.
    #(r'^$', portal_main_page),
    # url(r'^$', portal_main_page, name='portal_main_page'),
    url(
                           r'^json/$',
                           CalendarJsonListView.as_view(),
                           name='calendar_json'
                       ),
                       url(
                           r'^$',
                           CalendarView.as_view(),
                           name='calendar'
                       ),
    #url(r'^$', file_page, name='file_page'),

)