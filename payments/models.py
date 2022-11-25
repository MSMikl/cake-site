from django.db import models
import yookassa
from yookassa import Configuration, Payment
from yookassa.domain.common import Version

from cakes import settings


class OrderPayment(models.Model):

    payment_id = models.CharField('ID заказа', max_length=255)
    payment_status = models.CharField('Статус оплаты', max_length=100)

    class Meta:
        verbose_name = 'Оплата заказа'
        verbose_name_plural = 'Оплаты заказов'

    def __str__(self) -> str:
        return self.order_id

    def create_payment(self, amount, return_url, description, order_number, customer_name, customer_email, customer_phone):

        Configuration.configure(settings.SHOP_ID, settings.SHOP_API_KEY)

        Configuration.configure_user_agent(
            framework=Version('Django', '4.1.3')
        )

        payment_response = Payment.create(
            {
                "amount": {
                    "value": amount,
                    "currency": "RUB"
                },
                "confirmation": {
                    "type": "redirect",
                    "return_url": return_url
                },
                "capture": True,
                "description": description,
                "metadata": {
                    'orderNumber': order_number
                },
                "receipt": {
                    "customer": {
                        "full_name": customer_name,
                        "email": customer_email,
                        "phone": customer_phone,
                        "inn": "0"
                    },
                    "items": [
                        {
                            "description": description,
                            "quantity": "1.00",
                            "amount": {
                                "value": amount,
                                "currency": "RUB"
                            },
                            "vat_code": "2",
                            "payment_mode": "full_payment",
                            "payment_subject": "commodity",
                            "country_of_origin_code": "CN",
                            "product_code": "44 4D 01 00 21 FA 41 00 23 05 41 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00 12 00 AB 00",
                            "customs_declaration_number": "10714040/140917/0090376",
                            "excise": "20.00",
                            "supplier": {
                                "name": "string",
                                "phone": "string",
                                "inn": "string"
                            }
                        },
                    ]
                }
            }
        )

        self.payment_id = payment_response['id']

        return payment_response

    def check_payment_status(self, payment_id):

        response = Payment.find_one(payment_id)

        self.payment_status = response['status']

        return response

