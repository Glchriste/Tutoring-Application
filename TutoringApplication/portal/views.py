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
            recipients = ['wevie13@gmail.com']
            #Send Email with data
            from django.core.mail import send_mail
            send_mail('Tutoring Appointment Scheduled', comment, email, recipients)


            return HttpResponseRedirect(reverse('portal:portal_main_page'))
            #return render_to_response('portal/index.html')
    else:
        form = AppointmentForm()
 
    data = {'form': form}
    return render_to_response('portal/index.html', data, context_instance=RequestContext(request))