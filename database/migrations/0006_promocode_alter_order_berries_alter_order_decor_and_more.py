# Generated by Django 4.1.3 on 2022-11-25 15:57

from django.db import migrations, models
import django.db.models.deletion
import django.utils.timezone


class Migration(migrations.Migration):

    dependencies = [
        ('database', '0005_order_payment_id_alter_order_status'),
    ]

    operations = [
        migrations.CreateModel(
            name='Promocode',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('text', models.CharField(max_length=50, verbose_name='Текст промокода')),
                ('discount', models.DecimalField(decimal_places=2, max_digits=5, verbose_name='Скидка в %')),
                ('is_active', models.BooleanField(default=False, verbose_name='Активен')),
                ('active_date', models.DateTimeField(default=django.utils.timezone.now, verbose_name='Дата окончания действия')),
            ],
        ),
        migrations.AlterField(
            model_name='order',
            name='berries',
            field=models.ForeignKey(default='1', on_delete=django.db.models.deletion.SET_DEFAULT, related_name='orders', to='database.berries', verbose_name='Ягоды'),
        ),
        migrations.AlterField(
            model_name='order',
            name='decor',
            field=models.ForeignKey(default='1', on_delete=django.db.models.deletion.SET_DEFAULT, related_name='orders', to='database.decor', verbose_name='Украшение'),
        ),
        migrations.AlterField(
            model_name='order',
            name='layers',
            field=models.ForeignKey(null=True, on_delete=django.db.models.deletion.SET_NULL, related_name='orders', to='database.layer', verbose_name='Количество слоев'),
        ),
        migrations.AlterField(
            model_name='order',
            name='shape',
            field=models.ForeignKey(null=True, on_delete=django.db.models.deletion.SET_NULL, related_name='orders', to='database.shape', verbose_name='Форма'),
        ),
        migrations.AlterField(
            model_name='order',
            name='topping',
            field=models.ForeignKey(default='1', on_delete=django.db.models.deletion.SET_DEFAULT, related_name='orders', to='database.topping', verbose_name='Топпинг'),
        ),
        migrations.AddField(
            model_name='order',
            name='promocode',
            field=models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.SET_NULL, related_name='orders', to='database.promocode', verbose_name='Промокод'),
        ),
    ]