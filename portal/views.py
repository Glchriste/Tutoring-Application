#from django.shortcuts import render
from django.http import HttpResponseRedirect
from django.template import RequestContext
from django.core.urlresolvers import reverse
from django.shortcuts import render_to_response
from django.contrib.auth.decorators import login_required

from forms import AppointmentForm
from forms import PostForm
from models import UploadFile
from django.http import HttpResponse
from django.shortcuts import render
from models import CalendarEvent
from datetime import datetime, timedelta

from django.shortcuts import redirect
from django.core.mail import send_mail
#############################################
# Calendar Form Test
#############################################


### Displays an appointment form
def appt_form(request):
    return render(request, 'portal/index.html')

def make_appt(request):
    #Appointment Form Input Values
    first_name = ''
    last_name = ''
    email = ''
    course = ''
    date = ''
    time = ''
    tutor = ''
    message = ''

    if 'first_name' in request.POST:
        first_name = request.POST['first_name']
        message += 'Your first name: %r' % request.POST['first_name']
    else:
        message = 'Please enter your first name.'
    if 'last_name' in request.POST:
        last_name = request.POST['last_name']
        message += '<br></br>Your last name: %r' % last_name
    else:
        message = 'Please enter your last name.'
    if 'email' in request.POST:
        email = request.POST['email']
        message += '<br></br>Your email: %r' % email
    else:
        message = 'Please enter your UNCC email.'
    if 'course' in request.POST:
        course = request.POST['course']
        message += '<br></br>Your course: %r' % course
    else:
        message = 'Please select enter a course you need help with.'
    if 'date' in request.POST:
        date = request.POST['date']
        message += '<br></br>Your date: %r' % date
    else:
        message = 'Please enter a date.'
    if 'time' in request.POST:
        time = request.POST['time']
        message += '<br></br>Your time: %r' % time
    else:
        message = 'Please enter a time.'
    if 'tutor' in request.POST:
        tutor = request.POST['tutor']
        if tutor == 'no_preference':
            tutor = 'Anyone Available'
        else:
            message += '<br></br>Your tutor: %r' % tutor
    else:
        message = 'Please enter a tutor.'

    #Converting DatePicker input to datetime format
    dateConvert = {'01': 'Jan', '02': 'Feb', '03': 'Mar', '04': 'Apr', '05': 'May', '06':'Jun', '07':'Jul', '08':'Aug', '09':'Sep', '10':'Oct', '11':'Nov', '12':'Dec'}
    date_list = date.split('/')
    #month = str(dateConvert[str(date_list[0])])
    month = str(date_list[0])
    day = str(date_list[1])
    year = str(date_list[2])
    date_string = month + ' ' + day + ' ' + year
    date_input = date_string + ' ' + time

    message += '<br><br> Date String: %r' % date_string
    message += '<br><br> Date Input: %r' % date_input
    try:
        start = datetime.datetime.strptime(str(date + ' ' + time), '%m/%d/%Y %I:%M%p')
        end = start + timedelta(hours=1)
    except:
        start = None
        end = None

    tutor_emails = {'Grace': 'gchriste@uncc.edu'}

    try:
        event = CalendarEvent()
        title = 'Tutoring Appointment for ' + first_name + ' ' + last_name + ' with ' + tutor + ' at ' + time
        event.title = title
        event.tutor = tutor
        event.tutor_email = tutor_emails[tutor]
        event.student = first_name + ' ' + last_name
        event.course = course
        event.start = start
        event.end = end
        message = str(event) + ': <br></br>' + message
        event.save()
        message = 'Success! Thank you for scheduling your appointment with CCI Tutors!'
        recipients = ['glchriste@gmail.com']
        send_mail('Tutoring Appointment Scheduled', 'Confirming CCI ' + title, student_email, recipients)
        send_mail('Tutoring Appointment Scheduled', 'Confirming CCI ' + title, tutor_emails[tutor], recipients)
    except:
        message = 'Form submission failed (form submitted without all needed data to create a Calendar Event).'

    # return HttpResponse(message)
    return redirect('/portal')

#############################################
# Form Test
#############################################

### Displays a search form
def search_form(request):
    return render(request, 'search_form.html')

### Function to search for whatever term the user entered via the request
def search(request):
    #Handles the GET request
    if 'q' in request.GET:
        message = 'You searched for: %r' % request.GET['q'] #Returns what the user searched for
    else:
        message = 'You submitted an empty form.'
    return HttpResponse(message) #Return an HttpResponse with the result message

#############################################
# Main Calendar View
#############################################
@login_required
def portal_main_page(request):
    if request.method == 'POST':
        # form = AppointmentForm(request.POST, request.FILES)
#         if form.is_valid():
#             email = form.cleaned_data['email']
#             course = form.cleaned_data['course']
#             date = form.cleaned_data['date']
#             comment = form.cleaned_data['comment']
# # <<<<<<< HEAD:portal/views.py
#             recipients = ['glchriste@gmail.com', 'wevie13@gmail.com']
# # =======
# #             recipients = ['wevie13@gmail.com']
# # >>>>>>> a5577930ebce31881ed307749d7fa01d02b92d19:TutoringApplication/portal/views.py
#             #Send Email with data
#             from django.core.mail import send_mail
#             send_mail('Tutoring Appointment Scheduled', comment, email, recipients)


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

#############################################
# Converts calendar events to JSON list
#############################################

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