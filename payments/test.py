import var_dump as var_dump
import yookassa
from yookassa import Configuration, Settings, Payment
from yookassa.domain.common import Version

from cakes import settings

Configuration.configure(settings.SHOP_ID, settings.SHOP_API_KEY)

Configuration.configure_user_agent(
    framework=Version('Django', '4.1.3')
)

me = Settings.get_account_settings()
var_dump.var_dump(me)

'''
res = Payment.create(
    {
        "amount": {
            "value": 1000,
            "currency": "RUB"
        },
        "confirmation": {
            "type": "redirect",
            "return_url": "https://merchant-site.ru/return_url"
        },
        "capture": True,
        "description": "Заказ №72",
        "metadata": {
            'orderNumber': '72'
        },
        "receipt": {
            "customer": {
                "full_name": "Ivanov Ivan Ivanovich",
                "email": "email@email.ru",
                "phone": "79211234567",
                "inn": "6321341814"
            },
            "items": [
                {
                    "description": "Переносное зарядное устройство Хувей",
                    "quantity": "1.00",
                    "amount": {
                        "value": 1000,
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

var_dump.var_dump(res)
'''

res = Payment.find_one('2b110d0c-000f-5000-a000-1cec0345c12b')

var_dump.var_dump(res)
