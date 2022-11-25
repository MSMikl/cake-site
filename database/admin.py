from django.contrib import admin
from django.contrib.admin.views.main import ChangeList

from .models import Customer, Order, Decor, Shape, Layer, Topping, Berries

# Register your models here.

@admin.register(Customer)
class CutomerAdmin(admin.ModelAdmin):
    list_display = ['__str__', 'phone_number']
    list_display_links = ['__str__', 'phone_number']
    exclude = ['last_login', 'groups', 'user_permissions', 'password']
    readonly_fields = ['is_superuser', 'date_joined']


class MyChangeList(ChangeList):
    def get_results(self, request) -> None:
        super().get_results(request)
        self.total = sum(self.result_list.values_list('price', flat=True))


@admin.register(Order)
class OrderAdmin(admin.ModelAdmin):
    exclude = ['payment_id']
    list_display = ['__str__', 'price', 'user', 'creation_date', 'status']
    list_filter = ['status', 'user', 'creation_date']

    def get_changelist(self, request, **kwargs):
        return MyChangeList


@admin.register(Layer)
class LayerAdmin(admin.ModelAdmin):
    list_display = ['__str__', 'price', 'orders_count']


@admin.register(Shape)
class ShapeAdmin(admin.ModelAdmin):
    list_display = ['__str__', 'price', 'orders_count']


@admin.register(Topping)
class ToppingAdmin(admin.ModelAdmin):
    list_display = ['__str__', 'price', 'orders_count']


@admin.register(Berries)
class BerriesAdmin(admin.ModelAdmin):
    list_display = ['__str__', 'price', 'orders_count']


@admin.register(Decor)
class DecorAdmin(admin.ModelAdmin):
    list_display = ['__str__', 'price', 'orders_count']
