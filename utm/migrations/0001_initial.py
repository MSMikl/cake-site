# Generated by Django 4.1.3 on 2022-11-25 17:09

from django.db import migrations, models


class Migration(migrations.Migration):

    initial = True

    dependencies = [
    ]

    operations = [
        migrations.CreateModel(
            name='UtmCheck',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('check_in_date', models.DateTimeField(auto_now=True, verbose_name='Время захода')),
            ],
            options={
                'verbose_name': 'UTM метка',
                'verbose_name_plural': 'UTM метки',
            },
        ),
    ]
