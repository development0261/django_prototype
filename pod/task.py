from unicodedata import name

from celery import shared_task 
from celery.utils.log import get_task_logger


logger = get_task_logger(__name__)


from rest_framework.decorators import api_view
from .models import *
from django.core import serializers
from rest_framework.response import Response
import datetime
import requests

@shared_task
def update_task():
    company = Company.objects.first()
    company_name = company.name
    company.web_content_size = 90
    company.last_processed_date = datetime.datetime.now()
    print("HELLO")
    company.save()
    