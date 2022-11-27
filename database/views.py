import json
import requests
import uuid

from datetime import datetime
from random import choice
from requests.auth import HTTPBasicAuth

from django.conf import settings
from django.contrib.auth import authenticate, login, logout
from django.http import HttpResponse, JsonResponse
from django.shortcuts import render, redirect
from django.views import View
from django.views.decorators.csrf import csrf_exempt
from django.views.generic.edit import UpdateView
from django.urls import reverse
from django.utils import timezone

from utm.views import check_utm
from .models import Order, Layer, Shape, Topping, Berries, Decor, Customer, Promocode


class IndexView(View):
    def get(self, request):
        layers = Layer.objects.filter(available=True)

        check_utm(request)

        context = {
            'layers': layers,
            'shapes': Shape.objects.filter(available=True),
            'toppings': Topping.objects.filter(available=True),
            'berries': Berries.objects.filter(available=True),
            'decors': Decor.objects.filter(available=True),
        }
        return render(request, 'index.html', context=context)

    def post(self, request):
        print(request.POST)
        return redirect('index')


class LKView(UpdateView):

    model = Customer
    fields = ['name', 'phone_number']
    template_name = 'lk.html'
    success_url = '.'

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['orders'] = Customer.objects.filter(id=self.request.user.id).first().orders.all()
        return context

    def get_object(self):
        return Customer.objects.filter(id=self.request.user.id).first()


def generate_password(digits=4):
    password = ''
    string = '0123456789'
    for _ in range(digits):
        password += choice(string)
    return password


def send_message(text):
    url = f'https://api.telegram.org/bot{settings.TG_TOKEN}/sendMessage'
    data = {
        'text': text,
        'chat_id': settings.TG_CHAT_ID,
    }
    response = requests.post(url, json=data)
    response.raise_for_status()


class RegisterView(View):

    def get(self, request):
        phone_number = request.GET.get('phone_number')
        print(phone_number)
        user, created = Customer.objects.get_or_create(phone_number=phone_number)
        print(user)
        code = generate_password()
        send_message(code)
        user.set_password(code)
        user.save()
        return JsonResponse({'name': user.name if user.name else 'Noname'})

    def post(self, request):
        print(request.POST)
        phone_number = request.POST.get('phone_number')
        code = request.POST.get('code')
        user = authenticate(phone_number=phone_number, password=code)
        if user:
            login(request, user)
            return redirect('index')


class LoginView(View):
    def get(self, request):
        phone_number = request.GET.get('phone_number')
        code = request.GET.get('code')
        user = authenticate(phone_number=phone_number, password=code)
        if user:
            login(request, user)

        return HttpResponse('success')


class LogoutView(View):
    def get(self, request):
        logout(request)
        return redirect('index')


class MakeOrderView(View):
    def post(self, request):
        if request.user.is_authenticated:
            user = Customer.objects.get(phone_number=request.user.phone_number)
        else:
            user = Customer.objects.get_or_create(phone_number=request.POST.get('PHONE'))[0]
            login(request, user)
        name = request.POST.get('NAME')
        if name:
            user.name = name
            user.save()
        d_date = request.POST.get('DATE', '1970-01-01')
        d_time = request.POST.get('TIME', '00:00')
        promocode = request.POST.get('promocode')
        price = int(request.POST.get('COST', 10000))
        if promocode:
            code = Promocode.objects.filter(text=promocode, is_active=True, active_date__gte=timezone.now()).last()
            if code:
                price = price*code.discount/100
        order = Order(
            user=user,
            layers_id=request.POST.get('LEVELS'),
            shape_id=request.POST.get('FORM'),
            topping_id=request.POST.get('TOPPING'),
            berries_id=request.POST.get('BERRIES', '1'),
            decor_id=request.POST.get('DECOR', '1'),
            text=request.POST.get('WORDS', '1'),
            comments=request.POST.get('COMMENTS', ''),
            price=price,
            address=request.POST.get('ADDRESS'),
            delivery_details=request.POST.get('DELIVCOMMENTS'),
            delivery_date=datetime.strptime(f"{d_date}-{d_time}", "%Y-%m-%d-%H:%M")
        )
        url = 'https://api.yookassa.ru/v3/payments'
        uuid_key = str(uuid.uuid4())
        data = {
            "amount": {
            "value": order.price,
            "currency": "RUB"
            },
            "payment_id": uuid_key,
            "capture": True,
                "confirmation": {
                "type": "redirect",
                "return_url": f"https://{request.get_host()}{reverse('lk')}",
                },
            "description": "Заказ №1"
        }
        headers = {
            "Idempotence-Key": uuid_key,
            "Content-Type": "application/json",
        }
        auth = HTTPBasicAuth(settings.SHOP_ID, settings.SHOP_TOKEN)
        response = requests.post(url, json=data, headers=headers, auth=auth)
        response.raise_for_status()
        payment_data = response.json()
        payment_url = payment_data.get('confirmation', {}).get('confirmation_url')
        order.payment_id = payment_data.get('id')
        order.save()
        return redirect(payment_url)


@csrf_exempt
def callback_post(request):
    if request.method == 'POST':
        data = json.loads(request.body)
        id = data['object']['id']
        order = Order.objects.get(payment_id=id)
        if data.get('event') == 'payment.succeeded':
            order.status = Order.PREPARING
            order.save()
            text = f"Оплата заказа {order.number} прошла успешно. Мы уже готовим ваш заказ"
        elif data.get('event') == 'payment.canceled':
            text = f"Оплата заказа {order.number} отменена"
        send_message(text)
        return HttpResponse(status=200)


@csrf_exempt
def count_promocode(request):
    if request.method == 'GET':
        code = request.GET.get('PROMOCODE')
        discount = 0
        correct = False
        if code:
            promocode = Promocode.objects.filter(text=code, is_active=True, active_date__gte=timezone.now()).last()
            if promocode:
                correct = True
                discount = promocode.discount/100
        return JsonResponse({'correct': correct, 'discount': discount})


def post_feedback(request):
    if request.method == 'POST':
        number = request.POST.get('order_number')
        feedback = request.POST.get('feedback')
        order = Order.objects.get(number=number)
        order.feedback = feedback
        order.save()
        text = f"""
Покупатель {order.user.name} оставил обратную связь по заказу номер {order.number}
Текст комментария:
{feedback}
        """
        send_message(text)
        return redirect('lk')
