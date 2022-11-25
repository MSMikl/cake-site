import datetime

import requests
from django.shortcuts import render, redirect
import requests
from django.urls import reverse

from cakes import settings
from utm.models import UtmCheckin


def check_utm(request):

    get_referer = request.GET.get('utm_source')

    if not get_referer:
        return reverse('index')

    UtmCheckin.objects.create(
        check_in_date=datetime.datetime.now(),
        utm_source=request.GET.get('utm_source'),
        utm_medium=request.GET.get('utm_medium'),
        utm_campaign=request.GET.get('utm_campaign'),
        utm_content=request.GET.get('utm_content'),
        utm_term=request.GET.get('utm_term')
    )

    return reverse('index')


def send_message(text):
    url = f'https://api.telegram.org/bot{settings.TG_TOKEN}/sendMessage'
    data = {
        'text': text,
        'chat_id': settings.TG_CHAT_ID,
    }
    response = requests.post(url, json=data)
    response.raise_for_status()
