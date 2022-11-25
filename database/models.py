from django import forms
from django.contrib.auth.models import AbstractUser, BaseUserManager
from django.db import models
from django.forms import ModelForm
from django.utils import timezone

# Create your models here.


class CustomerManager(BaseUserManager):
    def create_user(self, name, phone_number, password=None, **extra_fields):
        if not name:
            raise ValueError('Необходимо указать имя')
        if not phone_number:
            raise ValueError('Необходимо указать номер телефона')
        user = self.model(name=name, phone_number=phone_number, **extra_fields)
        user.set_password(password)
        user.save()
        return user

    def create_superuser(self, name, phone_number,  password, **extra_fields):
        extra_fields.setdefault('is_staff', True)
        extra_fields.setdefault('is_superuser', True)
        extra_fields.setdefault('is_active', True)
        return self.create_user(name, phone_number, password, **extra_fields)


class Customer(AbstractUser):
    username = None
    email = None
    first_name = None
    last_name = None
    name = models.CharField(
        'Имя покупателя',
        max_length=100,
        default='',
        blank=True,
    )
    phone_number = models.CharField(
        'Номер телефона',
        max_length=20,
        unique=True,
    )
    address = models.CharField(
        'Адрес',
        max_length=300,
        null=True,
        blank=True,
    )
    date_joined = models.DateTimeField(
        'Дата регистрации',
        default=timezone.now
    )
    REQUIRED_FIELDS = ['name']
    USERNAME_FIELD = 'phone_number'

    objects = CustomerManager()

    def __str__(self) -> str:
        return self.name

    class Meta:
        verbose_name = 'Покупатель'
        verbose_name_plural = 'Покупатели'


class Order(models.Model):
    PAYMENT = 'Payment'
    PREPARING = 'Preparing'
    IN_DELIVERY = 'In delivery'
    COMPLETED = 'Completed'

    STATUSES = [
        (PAYMENT, 'Ожидает оплаты'),
        (PREPARING, 'Готовится'),
        (IN_DELIVERY, 'Доставляется'),
        (COMPLETED, 'Завершен'),
    ]

    number = models.AutoField(
        'Номер заказа',
        primary_key=True,
        unique=True
    )
    user = models.ForeignKey(
        'Customer',
        on_delete=models.SET_NULL,
        null=True,
        related_name='orders',
        verbose_name='Заказчик'
    )
    layers = models.ForeignKey(
        'Layer',
        verbose_name='Количество слоев',
        on_delete=models.SET_NULL,
        related_name='orders',
        null=True,
    )
    shape = models.ForeignKey(
        'Shape',
        on_delete=models.SET_NULL,
        related_name='orders',
        null=True,
        verbose_name='Форма'
    )
    topping = models.ForeignKey(
        'Topping',
        on_delete=models.SET_DEFAULT,
        related_name='orders',
        default='1',
        verbose_name='Топпинг'
    )
    berries = models.ForeignKey(
        'Berries',
        on_delete=models.SET_DEFAULT,
        related_name='orders',
        default='1',
        verbose_name='Ягоды'
    )
    decor = models.ForeignKey(
        'Decor',
        on_delete=models.SET_DEFAULT,
        related_name='orders',
        default='1',
        verbose_name='Украшение'
    )
    text = models.CharField(
        'Надпись на торте',
        max_length=100,
        blank=True
    )
    comments = models.TextField(
        'Комментарий',
        blank=True
    )
    price = models.DecimalField(
        'Цена',
        default=0,
        max_digits=10,
        decimal_places=2
    )
    promocode = models.ForeignKey(
        'Promocode',
        on_delete=models.SET_NULL,
        verbose_name='Промокод',
        related_name='orders',
        null=True,
        blank=True,
    )
    creation_date = models.DateTimeField(
        'Дата создания заказа',
        default=timezone.now,
    )
    address = models.TextField(
        'Адрес доставки',
        blank=True,
        default=''
    )
    status = models.CharField(
        'Статус заказа',
        max_length=20,
        choices=STATUSES,
        default=PAYMENT,
    )
    delivery_date = models.DateTimeField(
        'Дата и время доставки',
        default=None,
        null=True,
        blank=True
    )
    delivery_details = models.TextField(
        'Комментарии для курьера',
        blank=True,
        default='',
    )
    payment_id = models.CharField(
        'id оплаты',
        max_length=50,
        null=True,
        blank=True,
    )

    def __str__(self) -> str:
        return f"Заказ номер {self.number}"

    class Meta:
        verbose_name = 'Заказ'
        verbose_name_plural = 'Заказы'


class Layer(models.Model):
    num_layers = models.IntegerField(
        'Количество слоев',
    )
    price = models.DecimalField(
        'Цена',
        max_digits=6,
        decimal_places=2,
        null=True,
        default=0
    )
    image = models.ImageField(
        'Изображение',
        null=True,
        blank=True,
    )
    available = models.BooleanField(
        'Доступно к заказу',
        default=True,
    )

    def orders_count(self):
        return self.orders.count()

    @property
    def int_price(self):
        return int(self.price)

    def __str__(self) -> str:
        return f"{self.num_layers}"

    class Meta:
        verbose_name = 'Опция количества слоев'
        verbose_name_plural = 'Опции количества слоев'


class Shape(models.Model):
    name = models.CharField(
        'Описание формы',
        max_length=100,
    )

    price = models.DecimalField(
        'Цена',
        max_digits=6,
        decimal_places=2,
        null=True,
        default=0
    )
    image = models.ImageField(
        'Изображение',
        null=True,
        blank=True,
    )
    available = models.BooleanField(
        'Доступно к заказу',
        default=True,
    )
    
    def orders_count(self):
        return self.orders.count()

    @property
    def int_price(self):
        return int(self.price)

    def __str__(self) -> str:
        return f"{self.name}"

    class Meta:
        verbose_name = 'Опция формы'
        verbose_name_plural = 'Опции формы'


class Topping(models.Model):
    name = models.CharField(
        'Описание топпинга',
        max_length=100,
    )

    price = models.DecimalField(
        'Цена',
        max_digits=6,
        decimal_places=2,
        null=True,
        default=0
    )
    image = models.ImageField(
        'Изображение',
        null=True,
        blank=True,
    )
    available = models.BooleanField(
        'Доступно к заказу',
        default=True,
    )
    
    def orders_count(self):
        return self.orders.count()

    @property
    def int_price(self):
        return int(self.price)

    def __str__(self) -> str:
        return f"{self.name}"

    class Meta:
        verbose_name = 'Опция топпинга'
        verbose_name_plural = 'Опции топпинга'


class Berries(models.Model):
    name = models.CharField(
        'Описание ягод',
        max_length=100,
    )

    price = models.DecimalField(
        'Цена',
        max_digits=6,
        decimal_places=2,
        null=True,
        default=0
    )
    image = models.ImageField(
        'Изображение',
        null=True,
        blank=True,
    )
    available = models.BooleanField(
        'Доступно к заказу',
        default=True,
    )
    
    def orders_count(self):
        return self.orders.count()

    @property
    def int_price(self):
        return int(self.price)

    def __str__(self) -> str:
        return f"{self.name}"

    class Meta:
        verbose_name = 'Опция ягод'
        verbose_name_plural = 'Опции ягод'


class Decor(models.Model):
    name = models.CharField(
        'Описание украшения',
        max_length=100,
    )

    price = models.DecimalField(
        'Цена',
        max_digits=6,
        decimal_places=2,
        null=True,
        default=0,
    )
    image = models.ImageField(
        'Изображение',
        null=True,
        blank=True,
    )
    available = models.BooleanField(
        'Доступно к заказу',
        default=True,
    )
    
    def orders_count(self):
        return self.orders.count()

    @property
    def int_price(self):
        return int(self.price)

    def __str__(self) -> str:
        return f"{self.name}"

    class Meta:
        verbose_name = 'Опция украшения'
        verbose_name_plural = 'Опции украшения'


class Promocode(models.Model):
    text = models.CharField(
        'Текст промокода',
        max_length=50,
    )
    discount = models.DecimalField(
        'Скидка в %',
        decimal_places=2,
        max_digits=5,
    )
    is_active = models.BooleanField(
        'Активен',
        default=False,
    )
    active_date = models.DateTimeField(
        'Дата окончания действия',
        default=timezone.now,
    )
    def __str__(self) -> str:
        return f"{self.text} на {int(self.discount)}%"

    class Meta:
        verbose_name = 'Промокод'
        verbose_name_plural = 'Промокоды'

