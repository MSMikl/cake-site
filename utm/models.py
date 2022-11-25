from django.db import models
from datetime import datetime


class UtmCheckin(models.Model):

    check_in_date = models.DateTimeField('Время захода', auto_now=True)
    utm_source = models.CharField('Источник UTM', max_length=100)
    utm_medium = models.CharField('Тип траффика', max_length=10)
    utm_campaign = models.CharField('Название компании', max_length=100)
    utm_content = models.CharField('Идентификатор объявления', max_length=250)
    utm_term = models.CharField('Ключевое слово', max_length=100)

    class Meta:
        verbose_name = 'UTM метка'
        verbose_name_plural = 'UTM метки'

    def __str__(self):
        return self.utm_source
