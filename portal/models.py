from django.db import models
from django.contrib.auth.models import User
import os
# Create your models here.
def get_upload_path(instance, filename):
	return os.path.join('files', instance.owner.username, filename)

class UploadFile(models.Model):
	#file = models.FileField(upload_to='files/%Y/%m/%d')
	file = models.FileField(upload_to=get_upload_path)

from django.utils.translation import ugettext as _
from utils import datetime_to_timestamp
from django.contrib import admin
import forms

# class Tutor(models.Model):
#     first_name = models.CharField(max_length=100, verbose_name=('First Name'))
#     last_name = models.CharField(max_length=100, verbose_name=('Last Name'))
#     email = models.EmailField(max_length=255, verbose_name=('Email'))

class CalendarEvent(models.Model):
    """
    Calendar Events
    """
    CSS_CLASS_CHOICES = (
        ('', _('Normal')),
        ('event-warning', _('Warning')),
        ('event-info', _('Info')),
        ('event-success', _('Success')),
        ('event-inverse', _('Inverse')),
        ('event-special', _('Special')),
        ('event-important', _('Important')),
    )
    title = models.CharField(max_length=255, verbose_name=_('Title'))
    tutor = models.CharField(max_length=50, verbose_name=('Tutor'))
    tutor_email = models.EmailField(max_length=255, verbose_name=('Tutor Email'))
    student = models.CharField(max_length=50, verbose_name=('Student'))
    student_email = models.EmailField(max_length=255, verbose_name=('Student Email'))
    course = models.CharField(max_length=50, verbose_name=('Course'))
    #url = models.URLField(verbose_name=_('URL'))
    url = 'http://www.example.com'
    #css_class = models.CharField(max_length=2,choices=CSS_CLASS_CHOICES,default='event-success')
    css_class = 'event-success'
    start = models.DateTimeField(verbose_name=_('Start Date'))
    end = models.DateTimeField(verbose_name=_('End Date'), blank=True)

    @property
    def start_timestamp(self):
        """
        Return end date as timestamp
        """
        return datetime_to_timestamp(self.start)

    @property
    def end_timestamp(self):
        """
        Return end date as timestamp
        """
        return datetime_to_timestamp(self.end)

    def __unicode__(self):
        return self.title

###Admin
class CalendarEventAdmin(admin.ModelAdmin):
    list_display = ["title", "tutor", "tutor_email", "student", "student_email", "css_class", "start", "end"]
    list_filler = ["title"]
    
admin.site.register(CalendarEvent,CalendarEventAdmin)