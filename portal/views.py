#from django.shortcuts import render
from django.http import HttpResponseRedirect
from django.template import RequestContext
from django.core.urlresolvers import reverse
from django.shortcuts import render_to_response
from django.contrib.auth.decorators import login_required

from forms import AppointmentForm
from models import UploadFile

# Create your views here.
@login_required
def portal_main_page(request):
    if request.method == 'POST':
        form = AppointmentForm(request.POST, request.FILES)
        if form.is_valid():
            email = form.cleaned_data['email']
            course = form.cleaned_data['course']
            date = form.cleaned_data['date']
            comment = form.cleaned_data['comment']
# <<<<<<< HEAD:portal/views.py
            recipients = ['glchriste@gmail.com', 'wevie13@gmail.com']
# =======
#             recipients = ['wevie13@gmail.com']
# >>>>>>> a5577930ebce31881ed307749d7fa01d02b92d19:TutoringApplication/portal/views.py
            #Send Email with data
            from django.core.mail import send_mail
            send_mail('Tutoring Appointment Scheduled', comment, email, recipients)


            return HttpResponseRedirect(reverse('portal:portal_main_page'))
            #return render_to_response('portal/index.html')
    else:
        form = AppointmentForm()
 
    data = {'form': form}
    return render_to_response('portal/index.html', data, context_instance=RequestContext(request))

from django.views.generic import ListView, TemplateView
from models import CalendarEvent
from serializers import event_serializer
from utils import timestamp_to_datetime

import datetime

#Converts calendar events to JSON list
class CalendarJsonListView(ListView):

    template_name = 'django_bootstrap_calendar/calendar_events.html'
    #Returns the calendar events as a JSON
    def get_queryset(self):
        queryset = CalendarEvent.objects.filter()
        from_date = self.request.GET.get('from', False)
        to_date = self.request.GET.get('to', False)

        if from_date and to_date:
            queryset = queryset.filter(
                start__range=(
                    timestamp_to_datetime(from_date) + datetime.timedelta(-30),
                    timestamp_to_datetime(to_date)
                    )
            )
        elif from_date:
            queryset = queryset.filter(
                start__gte=timestamp_to_datetime(from_date)
            )
        elif to_date:
            queryset = queryset.filter(
                end__lte=timestamp_to_datetime(to_date)
            )

        return event_serializer(queryset)


class CalendarView(TemplateView):

    template_name = 'portal/index.html'