from rest_framework.views import APIView
from rest_framework.response import Response
import re
import sys
import requests
from bs4 import BeautifulSoup
from django.http import HttpResponse
from rest_framework.serializers import ValidationError
from .models import Stock
from .serializers import StockSerializer
from rest_framework import viewsets
from rest_framework import status


class StockViews(APIView):

    # Поиск текста в теге ниже после регульярного выражения
    def get_data_by_regex(self, regexp, soup):
        match_string = soup.find(text=re.compile(r'\b{}'.format(regexp)))
        if not match_string is None:
            return match_string.find_next().text.strip()
        else:
            return "Данные отсутсвуют"

    # Проверка тикера на сушествование
    def get_tiker_status(self, stock):
        try:
            response = requests.get(
                "https://ru.tradingview.com/symbols/"+stock+"/")
            tiker = re.search('(?<=/symbols/).*?(?=/)', response.url)
            if response.status_code != 404:
                soup = BeautifulSoup(response.text, 'html.parser')
                stock_name = soup.find(
                    'div', class_='tv-symbol-header__first-line')
                stock_sector = self.get_data_by_regex('Сектор:', soup)
                stock_industry = self.get_data_by_regex('Отрасль:', soup)

                return({'status': 'found', 'message': 'Акция надена', 'url': response.url, 'tiker': tiker.group(0), 'stock_name': stock_name.text, 'stock_sector': stock_sector, 'stock_industry': stock_industry})
            else:
                return({'status': 'not_found', 'message': 'Акция не надена', 'url': response.url, 'tiker': tiker.group(0)})
        except requests.exceptions.ReadTimeout:
            print("Превышение времени ожидания ответа")
            sys.exit()

        except requests.exceptions.ConnectTimeout:
            print('Соединение с интернетом отсутсвует')
            sys.exit()

        except requests.exceptions.ConnectionError:
            print('Соединение с интернетом отсутсвует')
            sys.exit()

    # обработка POST add ticker

    def post(self, request):
        if request.data['stock']:

            # Извлекаем тикеры
            tickers = []
            data = request.data['stock'].split('\n')
            for tiker in data:
                if tiker:
                    ticker_status = self.get_tiker_status(tiker)

                    # Если тикер найден
                    if ticker_status['status'] == 'found':

                        # Проверка на дубликат
                        try:
                            found_stock_name = Stock.objects.get(
                                stock_name=ticker_status['stock_name'])

                        except Stock.DoesNotExist:
                            found_stock_name = None

                        # Дубликат наден
                        if found_stock_name != None:
                            tickers.append(
                                {'status': 'dublicate', 'tiker': ticker_status['tiker'], 'message': 'Идентификатор существует'})
                        else:
                            # Сохраним в базе
                            s = Stock(
                                stock_name=ticker_status['stock_name'],
                                stock_sector=ticker_status['stock_sector'],
                                stock_industry=ticker_status['stock_industry'],
                                stock_activity=True,
                                stock_identifier='',
                                stock_url=ticker_status['url'],
                            )
                            s.save()

                            # Проверка на созранение в базе?
                            if(s.pk):
                                tickers.append(ticker_status)
                    else:
                        # Тикер не найден
                        tickers.append(ticker_status)

            if not tickers:
                raise ValidationError(
                    [{'status': 'empty_value', 'message': 'Идентификаторы акции должны быть заполнены'}])
            else:
                return Response(tickers)
        else:
            raise ValidationError(
                [{'status': 'empty_value', 'message': 'Идентификаторы акции должны быть заполнены'}])

    # Обработка GET get ticker
    def get(self, request):
        queryset = Stock.objects.all().order_by('stock_name')
        serializer = StockSerializer(queryset, many=True)
        return Response(serializer.data)

     # Обработка DELETE get ticker
    def delete(self, request, id, format=None):
        print(id)
        Stock.objects.filter(
            id=id).update(stock_activity=False)

        # snippet = Stock.get_object(id)
        # snippet.delete()
        return Response(status=status.HTTP_204_NO_CONTENT)


def index(request):
    return HttpResponse("Hello, world.")
