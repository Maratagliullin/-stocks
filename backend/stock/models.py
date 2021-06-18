from django.db import models

# Create your models here.


class Stock(models.Model):
    stock_name = models.CharField(
        verbose_name='Наименование акции', max_length=50, unique=True)
    stock_sector = models.CharField(verbose_name='Сектор', max_length=200)
    stock_industry = models.CharField(verbose_name='Индустрия', max_length=200)
    stock_activity = models.BooleanField(verbose_name='Активность акции')
    investing_dentifier = models.CharField(
        verbose_name='Идентификатор investing.com', max_length=150, blank=True, null=True)
    tradingview_dentifier = models.CharField(
        verbose_name='Идентификатор tradingview.com', max_length=150, blank=True, null=True)
    stock_ticker = models.CharField(
        blank=True, null=True, max_length=50, verbose_name='Тикер')

    class Meta:
        verbose_name = 'Акции'
        verbose_name_plural = 'Акции'


class SourceDataCompany(models.Model):
    stock_ticker = models.CharField(
        verbose_name='Тикер', max_length=50)
    date = models.DateTimeField(verbose_name='Дата', auto_now_add=True)
    source_url = models.CharField(
        verbose_name='Ссылка на источник данных', blank=True, null=True, max_length=200)
    source = models.CharField(verbose_name='Источник данных', max_length=200)
    json_value = models.JSONField()

    class Meta:
        verbose_name = 'Исходные данные по компании'
        verbose_name_plural = 'Исходные данные по компании'
