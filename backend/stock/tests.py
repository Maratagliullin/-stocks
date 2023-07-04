import json

from django.test import Client, TestCase

from stock.tasks import get_investing_data, get_trading_data

from .models import Stock


class Test(TestCase):

    data = {
        'status': 'found',
        'message': 'Акция найдена',
        'tradingview_dentifier':
        'https://ru.tradingview.com/symbols/NASDAQ-AAPL/',
            'stock_ticker': 'NASDAQ-AAPL',
            'stock_name': 'Apple Inc',
            'stock_sector': 'Электронные технологии',
            'stock_industry': 'Телекоммуникационное оборудование',
            'investing_dentifier':
                'https://ru.investing.com/equities/apple-computer-inc',
    }

    def test_frontend(self):
        """Если клиентская часть развернулась,
        то получим http код ответа 200"""
        guest_client = Client()
        response = guest_client.get('http://localhost:8080/')
        self.assertEqual(response.status_code, 200)

    def test_backend(self):
        """Если бекенд часть развернулась,
        то при доступе к админ-панели получим с http код ответа 301 """
        guest_client = Client()
        response = guest_client.get('http://localhost:8000/admin')
        self.assertEqual(response.status_code, 301)

    def test_tradingview(self):
        """Проверка сервиса tradingview"""
        guest_client = Client()
        response = guest_client.get('http://ru.tradingview.com/')
        self.assertEqual(response.status_code, 200)

    def test_investing(self):
        """Проверка сервиса investing.com"""
        guest_client = Client()
        response = guest_client.get('http://investing.com/')
        self.assertEqual(response.status_code, 200)

    def test_create_ticker(self):
        """Проверка что известный тикер aapl буден найден"""
        guest_client = Client()
        resp = guest_client.post(
            'http://localhost:8000/api/v1/add_stock/', data={"stock": "aapl"})
        assert resp.json()[0]['status'] == "found"

    def test_store_ticker(self):
        """Проверка что найденный тикет сохранен в БД
        и сохраненные значения соответствуют входным данным """

        Stock.objects.create(
            tradingview_dentifier=self.data['tradingview_dentifier'],
            stock_ticker=self.data['stock_ticker'],
            stock_name=self.data['stock_name'],
            stock_sector=self.data['stock_sector'],
            stock_industry=self.data['stock_industry'],
            stock_activity=True,
        )
        self.assertEqual(Stock.objects.count(), 1)
        latest_row = Stock.objects.latest('id')
        self.assertEqual(latest_row.tradingview_dentifier,
                         self.data['tradingview_dentifier'])
        self.assertEqual(latest_row.stock_ticker, self.data['stock_ticker'])
        self.assertEqual(latest_row.stock_name, self.data['stock_name'])
        self.assertEqual(latest_row.stock_sector, self.data['stock_sector'])
        self.assertEqual(latest_row.stock_industry,
                         self.data['stock_industry'])

    def test_get_data_investing(self):
        """Проверка что мы получаем данные с investing.com
        и проверяем состав ключей с результирующей структурой"""

        Stock.objects.create(
            tradingview_dentifier=self.data['tradingview_dentifier'],
            investing_dentifier=self.data['investing_dentifier'],
            stock_ticker=self.data['stock_ticker'],
            stock_name=self.data['stock_name'],
            stock_sector=self.data['stock_sector'],
            stock_industry=self.data['stock_industry'],
            stock_activity=True,
        )

        result_dict = get_investing_data.apply().get(timeout=500)

        with open('stock/utills/data.json') as user_file:
            file_contents = user_file.read()
            parsed_json = json.loads(file_contents)

        for key in parsed_json.keys():
            assert key in result_dict[0]

    def test_get_data_tradingview(self):
        """Проверка что мы получаем данные tradingview
        проверяем наличие ключей в результирующей структуре,
        поскольку значения изменяемые"""

        Stock.objects.create(
            tradingview_dentifier=self.data['tradingview_dentifier'],
            stock_ticker=self.data['stock_ticker'],
            stock_name=self.data['stock_name'],
            stock_sector=self.data['stock_sector'],
            stock_industry=self.data['stock_industry'],
            stock_activity=True,
        )

        result_list = get_trading_data.apply().get(timeout=500)
        assert 'Рыночная капитализация' in result_list[0]
        assert 'Цена/Прибыль' in result_list[0]
        assert 'Код ISIN' in result_list[0]
        assert 'Сектор' in result_list[0]
        assert 'Дивидендный доход ' in result_list[0]
        assert 'Отрасль ' in result_list[0]
        assert 'Веб-сайт' in result_list[0]
        assert 'CEO' in result_list[0]
        assert 'Сотрудники' in result_list[0]
        assert 'Дата основания' in result_list[0]
        assert 'Главный офис' in result_list[0]
