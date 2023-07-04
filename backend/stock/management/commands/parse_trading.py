from django.db import transaction
from django.core.management.base import BaseCommand
import re
from bs4 import BeautifulSoup
from stock.models import SourceDataCompany
from stock.models import Stock
import requests


def get_data_by_regex(regexp, soup):
        match_string = soup.find('div',text=re.compile(r'\b{}'.format(regexp)))
        if not match_string is None:
            return match_string.find_next('div', class_=re.compile('value-.*')).text.strip()
        else:
            return "Данные отсутсвуют"


class Command(BaseCommand):
    help = 'Команда запуска парсинга tradingview'
    # Команда вызова обновления всех таблиц кодов из Россвязи

    def handle(self, *args, **options):
        # Константа отсутсвующих данных
        try:
            res = []
            stock_data = Stock.objects.filter(stock_activity=True)

            if stock_data:
                for item in stock_data:
                    tradingview_dentifier = item.tradingview_dentifier
                    response_tradingview = requests.get(tradingview_dentifier)
                    soup = BeautifulSoup(response_tradingview.text, 'html.parser')
                    data = {}

                    tags_main = soup.find(
                        'h1').getText()
                    if not tags_main is None:
                        market_index='Рыночная капитализация'
                        data[market_index] = get_data_by_regex(
                            market_index, soup)

                        market_index='Цена/Прибыль'
                        data[market_index] = get_data_by_regex(
                        market_index, soup)

                        market_index='Баз. прибыль на акцию'
                        data[market_index] = get_data_by_regex(
                        market_index, soup)

                        market_index='Код ISIN'
                        data[market_index] = get_data_by_regex(
                        market_index, soup)

                        market_index='Сектор'
                        data[market_index] = get_data_by_regex(
                        market_index, soup)

                        market_index='Дивидендный доход '
                        data[market_index] = get_data_by_regex(
                        market_index, soup)

                        market_index='Отрасль '
                        data[market_index] = get_data_by_regex(
                        market_index, soup)

                        market_index='Веб-сайт'
                        data[market_index] = get_data_by_regex(
                        market_index, soup)

                        market_index='CEO'
                        data[market_index] = get_data_by_regex(
                        market_index, soup)

                        market_index='Сотрудники'
                        data[market_index] = get_data_by_regex(
                        market_index, soup)

                        market_index='Дата основания'
                        data[market_index] = get_data_by_regex(
                        market_index, soup)

                        market_index='Главный офис'
                        data[market_index] = get_data_by_regex(
                        market_index, soup)

                        with transaction.atomic():
                            s = SourceDataCompany(
                                stock_ticker=item.stock_ticker,
                                source="Tradingview",
                                source_url=tradingview_dentifier,
                                json_value=data
                            )
                            s.save()
                    else:
                        with transaction.atomic():
                            s = SourceDataCompany(
                                stock_ticker=item.stock_ticker,
                                source="Tradingview",
                                source_url=tradingview_dentifier,
                                json_value={'status': 'Произошла ошибка'}
                            )
                            s.save()
                        return 'Произошла ошибка'
                    res.append(data)
                return res
            else:
                return 'There are no search data available on tradingview.com'
        except  Exception  as e:
            raise self.retry(exc=e)
