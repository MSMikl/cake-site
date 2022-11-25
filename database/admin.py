from django.contrib import admin

from .models import Customer, Order, Decor, Shape, Layer, Topping, Berries

# Register your models here.

@admin.register(Customer)
class CutomerAdmin(admin.ModelAdmin):
    list_display = ['__str__', 'phone_number']
    list_display_links = ['__str__', 'phone_number']
    exclude = ['last_login', 'groups', 'user_permissions', 'password']
    readonly_fields = ['is_superuser', 'date_joined']


@admin.register(Order)
class OrderAdmin(admin.ModelAdmin):
    exclude = ['payment_id']


@admin.register(Layer)
class LayerAdmin(admin.ModelAdmin):
    pass


@admin.register(Shape)
class ShapeAdmin(admin.ModelAdmin):
    pass


@admin.register(Topping)
class ToppingAdmin(admin.ModelAdmin):
    pass


@admin.register(Berries)
class BerriesAdmin(admin.ModelAdmin):
    pass


@admin.register(Decor)
class DecorAdmin(admin.ModelAdmin):
    pass
