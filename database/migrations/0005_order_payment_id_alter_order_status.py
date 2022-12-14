# Generated by Django 4.1.3 on 2022-11-25 04:37

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('database', '0004_remove_customer_first_name_remove_customer_last_name_and_more'),
    ]

    operations = [
        migrations.AddField(
            model_name='order',
            name='payment_id',
            field=models.CharField(blank=True, max_length=50, null=True, verbose_name='id оплаты'),
        ),
        migrations.AlterField(
            model_name='order',
            name='status',
            field=models.CharField(choices=[('Payment', 'Ожидает оплаты'), ('Preparing', 'Готовится'), ('In delivery', 'Доставляется'), ('Completed', 'Завершен')], default='Payment', max_length=20, verbose_name='Статус заказа'),
        ),
    ]
