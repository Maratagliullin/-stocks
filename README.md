# Мониторинг Акций

Парсинг основных показателей акций компаний и бухгалтерского баланса с tradingview и investing.com, формирование структуры данных для дальнейшего использования.

**Пример интерфейса:**
![Добавление акции](/frontend/src/assets/add_stock.png?raw=true "Добавление акции")
![Страница акции](/frontend/src/assets/stock_info.png?raw=true "Страница акции")
![Список акций](/frontend/src/assets/stock_list.png?raw=true "Список акций")
  
## Стек
**Бекэнд** - Django  
**Фронтенд** - Vue.js(Vuex)  

## Вспомогательные компоненты:    
**Selenoid/Selenium** - получние данных посредством запуска контейнера с браузером, ввиду постепенной(xhr) подгрузки данных на целевых сайтах  
**Bs4** - Библиотека парсинга  
**Celery** - Реализация очереди  


## Предварительный запуск  

В проект добавлен selenoid, необходимо предварительно скачать контейнеры с браузерами.  

Находясь в директории проекта на одном уровне с файлом `prepare_browsers.bash` выполнить команду:  
`sh prepare_browsers.bash`.

**Заполнить файлы переменных окружения своими параметрами!**  
.env - корневая дирректория, основные настройки бекенда  
.env - frontend/.env основные настройки фронтенда  

Находясь в директории проекта на одном уровне с файлом `docker-compose.local.yml` запустить:  
`docker-compose -f docker-compose.local.yml up`

**Фронтенд:** http://localhost:8080/  
**Бекенд:** http://localhost:8000/  
**Selenoid:** http://localhost:8081/  

**Учерные данные Django Admin:**  
**Логин:** administrator  
**Пароль:** adminpass  

Опрос тикера акции производится каждые 10 минут, этот параметр опционален и меняется в trading/settings.py, параметр `CELERY_BEAT_SCHEDULE`  

**Запуск тестов:**  
`docker exec stocks_backend_1 pytest -v`

**Пример файла переменных окружения local.env (файл переменных окружения):**  
```DJANGO_SETTINGS_MODULE=trading.settings
DJANGO_WSGI=trading.wsgi
PYTHONUNBUFFERED=1
DATABASE_URL=postgres://localdb:localdb@db:5432/localdb
POSTGRES_USER=localdb
POSTGRES_PASSWORD=localdb
POSTGRES_DB=localdb
REDIS_HOST=redis
C_FORCE_ROOT=true
SECRET_KEY==@ncgb%60i%044*9yu%*$^$55s+(-y#qj_+4ldra-syv!62yu@
DEBUG=True
DJANGO_ADMINISTRATOR_PASS=adminpass
```

**Для принудительного запуска задачи celery можно вызвать из django shell:**    
**get_investing_data** - получение данных с investing.com  
**get_trading_data** - получение данных с tradingview  
**get_investing_identify** - получение идентификатора с investing.com для последующего получения балансового отчета  

**Ручной запуск задач (команды исполняются построчно):** 
```docker exec -it stocks_backend_1 sh    
python3 manage.py shell  
from stock.tasks import get_investing_data,get_trading_data,get_investing_identify  
get_investing_identify.apply_async(countdown=30)  
get_investing_data.apply_async(countdown=30)  
get_trading_data.apply_async(countdown=30)
```





