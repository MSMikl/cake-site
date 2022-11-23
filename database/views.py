from django.shortcuts import render, redirect
from django.views import View
from django.views.generic.edit import FormView

from .models import Order, OrderForm, Layer, Shape, Topping, Berries, Decor, Customer

# Create your views here.

class IndexView(View):
    
    def get(self, request):
        layers = Layer.objects.filter(available=True)
        layers_prices = [0] + [int(value) for value in layers.values_list('price', flat=True)]
        print(layers_prices)
        context = {
            'layers': layers,
            'layers_prices': layers_prices,
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
