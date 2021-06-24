# Create your tasks here
from .models import Stock
from .models import SourceDataCompany
from celery import task
from celery import shared_task
from selenium import webdriver
from bs4 import BeautifulSoup
from celery.exceptions import MaxRetriesExceededError
from selenium.common.exceptions import WebDriverException, TimeoutException, NoSuchElementException
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.common.by import By
from selenium.webdriver.support.expected_conditions import _find_element
import json
import re
from django.db import transaction
import pickle


@shared_task(bind=True, default_retry_delay=5 * 60)
def get_investing_identify(self):
    try:
        res = []
        stock_data = Stock.objects.filter(investing_dentifier__isnull=True)
        if stock_data:
            for item in stock_data:
                stock_name = item.stock_name
                url_investing = "https://ru.investing.com/search/?q="+stock_name+"/"
                capabilities = {
                    "screenResolution": "1920x1080x24",
                    "browserName": "chrome",
                    "browserVersion": "91.0",
                    "selenoid:options": {
                        "enableVNC": False,
                        "enableVideo": False,
                        "sessionTimeout": "5m",
                    }
                }
                driver = webdriver.Remote(
                    command_executor='http://selenoid:4444/wd/hub', desired_capabilities=capabilities)

                driver.maximize_window()
                driver.get(url_investing)                
                soup_investing = BeautifulSoup(
                    driver.page_source, 'html.parser')
                driver.quit()
                search_result = soup_investing.find(
                    'a', class_='js-inner-all-results-quote-item')
                if not search_result is None:
                    investing_identify = search_result.get('href')

                    investing_identify = "https://ru.investing.com" + investing_identify
                else:
                    investing_identify = "Идентификатор не найден"
                with transaction.atomic():
                    item.investing_dentifier = investing_identify
                    item.save()
                res.append([stock_name, investing_identify])
            return res
        else:
            return 'There are no search data available on investing.com'
    except (TimeoutException, NoSuchElementException, WebDriverException, Exception, MaxRetriesExceededError) as e:
        raise self.retry(exc=e)
   


class text_to_change(object):

    def __init__(self, locator, empty_data):
        self.locator = locator
        self.empty_data = empty_data

    def __call__(self, driver):
        element_text = _find_element(driver, self.locator).text
        return element_text != self.empty_data


# Получние данных с tradingview.com
@shared_task(bind=True, default_retry_delay=5 * 60)
def get_trading_data(self):
    try:
        res = []
        stock_data = Stock.objects.filter(stock_activity=True)
        if stock_data:
            for item in stock_data:
                tradingview_dentifier = item.tradingview_dentifier
                stock_ticker = item.stock_ticker
                capabilities = {
                    "screenResolution": "1920x1080x24",
                    "browserName": "firefox",
                    "browserVersion": "89.0",
                    "selenoid:options": {
                        "enableVNC": False,
                        "enableVideo": False,
                        "sessionTimeout": "7m",
                    }
                }
                driver = webdriver.Remote(
                    command_executor='http://selenoid:4444/wd/hub', desired_capabilities=capabilities)
                driver.maximize_window()
                driver.get(tradingview_dentifier)  
                # Ожидание появления данных
                WebDriverWait(driver, 500).until(
                    text_to_change(
                        (By.CLASS_NAME, "tv-widget-fundamentals__value"), "-")
                )
                soup = BeautifulSoup(driver.page_source, 'html.parser')
                driver.quit()
                data = {}
                tags_main = soup.find_all(
                    'div', attrs={'class': 'tv-widget-fundamentals__item'})
                if not tags_main is None:
                    for tag in tags_main:
                        title = tag.find('div', attrs={'class': 'tv-widget-fundamentals__title'}).get_text(
                        ).replace('\n', '').replace('\r', '').replace('\t', '')
                        data_inside = {}
                        for tag_inner in tag.findAll('div', attrs={'class': 'tv-widget-fundamentals__row'}):
                            tag_label = tag_inner.find('span', attrs={'class': 'tv-widget-fundamentals__label'}).get_text(
                            ).replace('\n', '').replace('\r', '').replace('\t', '')
                            tag_value = tag_inner.find('span', attrs={'class': 'tv-widget-fundamentals__value'}).get_text(
                            ).replace('\n', '').replace('\r', '').replace('\t', '')
                            data_inside[tag_label] = tag_value
                        data[title] = data_inside

                    with transaction.atomic():
                        s = SourceDataCompany(
                            stock_ticker=stock_ticker,
                            source="Tradingview",
                            source_url=tradingview_dentifier,
                            json_value=data
                        )
                        s.save()
                else:
                    with transaction.atomic():
                        s = SourceDataCompany(
                            stock_ticker=stock_ticker,
                            source="Tradingview",
                            source_url=tradingview_dentifier,
                            json_value={'status': 'Произошла ошибка'}
                        )
                        s.save()
                    return 'Произошла ошибка'
                res.append(data)
            return res
        else:
            return 'There are no search data available on investing.com'
    except (TimeoutException, NoSuchElementException, WebDriverException, Exception, MaxRetriesExceededError) as e:
        raise self.retry(exc=e)

   


def clear_text(row):
    return row.get_text(
    ).replace('\n', '').replace('\r', '').replace('\t', '').strip()

# Получние данных с investing.com


@shared_task(bind=True, default_retry_delay=5 * 60)
def get_investing_data(self):
    try:
        res = []
        stock_data = Stock.objects.filter(
            stock_activity=True).exclude(investing_dentifier='Идентификатор не найден').exclude(investing_dentifier__isnull=True)
        if stock_data:
            for item in stock_data:
                investing_dentifier = item.investing_dentifier
                stock_ticker = item.stock_ticker
                capabilities = {
                    "screenResolution": "1920x1080x24",
                    "browserName": "chrome",
                    "browserVersion": "91.0",
                    "selenoid:options": {
                        "enableVNC": False,
                        "enableVideo": False,
                        "sessionTimeout": "5m",
                    }
                }
                driver = webdriver.Remote(
                    command_executor='http://selenoid:4444/wd/hub', desired_capabilities=capabilities)
                source_url = investing_dentifier+'-balance-sheet'
                driver.maximize_window()
                driver.get(source_url)
                soup = BeautifulSoup(driver.page_source, 'html.parser')
                driver.quit()
                # Заголовки с периодом
                table_header = soup.find('tr', attrs={'id': 'header_row'})
                if not table_header is None:
                    fin_table = []
                    table_header_items = table_header.find_all('th')
                    for table_header_item in table_header_items:
                        table_header = table_header_item.get_text()
                        table_header = re.sub(
                            r'(^[0-9]{4})', r'\1/', table_header)
                        fin_table.append(table_header)

                    # Ищем таблицу
                    find_table = soup.find(
                        'table', attrs={'class': ['reportTbl']})
                    tbody = find_table.find_all('tbody')
                    # Поиск строк с идентификатором parentTr которые отрадают глобальные блоки в таблице
                    table_rows = tbody[1].find_all('tr')

                    # Массив строк
                    row_object = {}
                    for table_row in table_rows:

                        # Значения конкретной строки
                        row_value = {}

                        # Проверка есть ли внутренная таблица строки
                        table_children = table_row.find(
                            'table')
                        if not table_children is None:

                            # Отбор всех строк внутреей таблицы
                            table_children_rows = table_children.find_all('tr')

                            # Перебор строк и отправки из в результирующую структуру
                            for table_children_row in table_children_rows:
                                table_children_row_values = table_children_row.find_all(
                                    'td')
                                k = 0
                                for table_children_row_value in table_children_row_values:
                                    if k != 0:
                                        row_value[fin_table[k].strip()] = clear_text(
                                            table_children_row_value)
                                    k += 1
                        else:

                            # Блок поиска конкретных значений в строке и упаковка в структуру table_data_value
                            table_parent_row_values = table_row.find_all('td',)
                            i = 0
                            for table_parent_row_value in table_parent_row_values:
                                if i != 0:
                                    row_value[fin_table[i].strip()] = clear_text(
                                        table_parent_row_values[i])
                                i += 1

                            row_object[clear_text(
                                table_parent_row_values[0])] = row_value
                    with transaction.atomic():
                        s = SourceDataCompany(
                            stock_ticker=stock_ticker,
                            source="Investing",
                            source_url=source_url,
                            json_value=row_object
                        )
                        s.save()
                else:
                    with transaction.atomic():
                        s = SourceDataCompany(
                            stock_ticker=stock_ticker,
                            source="Investing",
                            source_url=source_url,
                            json_value={'status': 'Произошла ошибка'}
                        )
                        s.save()
                    return 'Произошла ошибка'
                res.append(row_object)
            return res
        else:
            return 'There are no search data available on investing.com'
    except (TimeoutException, NoSuchElementException, WebDriverException, Exception, MaxRetriesExceededError) as e:
        raise self.retry(exc=e)
    
