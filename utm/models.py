from django.db import models
from datetime import datetime


class UtmCheck(models.Model):

    check_in_date = models.DateTimeField('Время захода', auto_now=True)

    class Meta:
        verbose_name = 'UTM метка'
        verbose_name_plural = 'UTM метки'

    def __str__(self) -> str:
        return self.check_in_date.strftime('%Y-%m-%d %H:%M')
