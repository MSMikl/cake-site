import requests
from django.shortcuts import render
import requests
from cakes import settings


def check_utm(request):

    get_referer = request.GET.get('utm_source')

    if not get_referer:
        return

    send_message(get_referer)

    return


def send_message(text):
    url = f'https://api.telegram.org/bot{settings.TG_TOKEN}/sendMessage'
    data = {
        'text': text,
        'chat_id': settings.TG_CHAT_ID,
    }
    response = requests.post(url, json=data)
    response.raise_for_status()
