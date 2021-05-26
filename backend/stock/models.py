from django.db import models

# Create your models here.


class Stock(models.Model):
    stock_name = models.CharField(
        verbose_name='Наименование акции', max_length=50, unique=True)
    stock_sector = models.CharField(verbose_name='Сектор', max_length=200)
    stock_industry = models.CharField(verbose_name='Индустрия', max_length=200)
    stock_activity = models.BooleanField(verbose_name='Активность акции')
    stock_identifier = models.CharField(
        verbose_name='Идентификатор', max_length=50)
