from django.db import models
import yookassa


class OrderPayment(models.Model):

    order_id = models.CharField('ID заказа', max_length=255)
    amount = models.DecimalField('Стоимость заказа', max_digits=8, decimal_places=2)
    description = models.CharField('Описание заказа', max_length=300)

    class Meta:
        verbose_name = 'Оплата заказа'
        verbose_name_plural = 'Оплаты заказов'

    def __str__(self) -> str:
        return self.order_id

    def create_payment(self):
        ...

