# Generated by Django 4.1.3 on 2022-11-23 08:30

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('database', '0001_initial'),
    ]

    operations = [
        migrations.CreateModel(
            name='Layer',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('num_layers', models.IntegerField(verbose_name='Количество слоев')),
                ('price', models.DecimalField(decimal_places=2, default=0, max_digits=6, null=True, verbose_name='Цена')),
                ('image', models.ImageField(blank=True, null=True, upload_to='', verbose_name='Изображение')),
                ('available', models.BooleanField(default=True, verbose_name='Доступно к заказу')),
            ],
            options={
                'verbose_name': 'Опция количества слоев',
                'verbose_name_plural': 'Опции количества слоев',
            },
        ),
        migrations.AddField(
            model_name='berries',
            name='available',
            field=models.BooleanField(default=True, verbose_name='Доступно к заказу'),
        ),
        migrations.AddField(
            model_name='decor',
            name='available',
            field=models.BooleanField(default=True, verbose_name='Доступно к заказу'),
        ),
        migrations.AddField(
            model_name='shape',
            name='available',
            field=models.BooleanField(default=True, verbose_name='Доступно к заказу'),
        ),
        migrations.AddField(
            model_name='topping',
            name='available',
            field=models.BooleanField(default=True, verbose_name='Доступно к заказу'),
        ),
        migrations.AlterField(
            model_name='order',
            name='layers',
            field=models.ForeignKey(null=True, on_delete=django.db.models.deletion.SET_NULL, to='database.layer', verbose_name='Количество слоев'),
        ),
        migrations.DeleteModel(
            name='Layers',
        ),
    ]
