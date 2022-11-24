from django.db import transaction
from django.core.management.base import BaseCommand

from database.models import Layer, Shape, Topping, Berries, Decor


class Command(BaseCommand):
    help = "Generates stub data"

    @transaction.atomic
    def handle(self, *args, **kwargs):
        self.stdout.write("Deleting old data...")
        Layer.objects.all().delete()
        Shape.objects.all().delete()
        Topping.objects.all().delete()
        Berries.objects.all().delete()
        Decor.objects.all().delete()
        self.stdout.write("Creating new data...")
        DATA = {
            'Layers': [(1, 400), (2, 750), (3, 1100)],
            'Shapes': [('Круг', 600), ('Квадрат', 400), ('Прямоугольник', 1000)],
            'Toppings': [
                ('Без', 0),
                ('Белый соус', 200),
                ('Карамельный', 180),
                ('Кленовый', 200),
                ('Черничный', 300),
                ('Молочный шоколад', 350),
                ('Клубничный', 200)
            ],
            'Berries': [
                ('Без', 0),
                ('Ежевика', 400),
                ('Малина', 300),
                ('Голубика', 450),
                ('Клубника', 500)
            ],
            'Decors': [
                ('Без', 0),
                ('Фисташки', 300),
                ('Безе', 400),
                ('Фундук', 350),
                ('Пекан', 300),
                ('Маршмеллоу', 200),
                ('Марципан', 280)
            ]
        }

        Layer.objects.bulk_create(
            [Layer(price=price, num_layers=value) for (value, price) in DATA['Layers']]
        )
        Shape.objects.bulk_create(
            [Shape(price=price, name=value) for (value, price) in DATA['Shapes']]
        )
        Topping.objects.bulk_create(
            [Topping(price=price, name=value) for (value, price) in DATA['Toppings']]
        )
        Berries.objects.bulk_create(
            [Berries(price=price, name=value) for (value, price) in DATA['Berries']]
        )
        Decor.objects.bulk_create(
            [Decor(price=price, name=value) for (value, price) in DATA['Decors']]
        )
