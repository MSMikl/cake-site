import requests

from datetime import datetime
from random import choice

from django.conf import settings
from django.contrib.auth import authenticate, login, logout
from django.http import HttpResponse, JsonResponse
from django.shortcuts import render, redirect
from django.views import View
from django.views.generic.edit import FormView

from .models import Order, OrderForm, Layer, Shape, Topping, Berries, Decor, Customer


class IndexView(View):
    def get(self, request):
        layers = Layer.objects.filter(available=True)
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


class LKView(View):

    def get(self, request):
        user = Customer.objects.filter(id=request.user.id).prefetch_related('orders').first()
        context = {
            'user': user,
            'orders': user.orders.all()
        }
        return render(request, 'lk.html', context=context)


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
        print(request.POST)
        if request.user:
            user = Customer.objects.get(phone_number=request.user.phone_number)
        else:
            user = Customer.objects.get_or_create(phone_number=request.POST.get('PHONE'))[0]
        name = request.POST.get('NAME')
        if name:
            user.name = name
            user.save()
        d_date = request.POST.get('DATE', '1970-01-01')
        d_time = request.POST.get('TIME', '00:00')
        order = Order(
            user=user,
            layers_id=request.POST.get('LEVELS'),
            shape_id=request.POST.get('FORM'),
            topping_id=request.POST.get('TOPPING'),
            berries_id=request.POST.get('BERRIES', '1'),
            decor_id=request.POST.get('DECOR', '1'),
            text=request.POST.get('WORDS', '1'),
            comments=request.POST.get('COMMENTS', ''),
            price=int(request.POST.get('COST', 0)),
            address=request.POST.get('ADDRESS'),
            delivery_details=request.POST.get('DELIVCOMMENTS'),
            delivery_date=datetime.strptime(f"{d_date}-{d_time}", "%Y-%m-%d-%H:%M")
        )
        order.save()
        print(order)
        url = 'https://yookassa.ru/integration/simplepay/payment'
        data = {
            "sum": order.price
        }
        response = requests.post(url, json=data)
        print(response)
