# Мониторинг Акций

Парсинг основных показателей акций компаний и бухгалтерского баланса с tradingview и investing.com, формирование структуры данных для дальнейшего использования.
  
## Стек
Бекэнд - Django
Фронтенд - Vue.js с Vuex

## Вспомогательные компоненты:    
Selenoid/Selenium - получние данных посредством запуска контейнера с браузером, ввиду постепенной(xhr) подгрузки данных на целевых сайтах
Bs4 - Библиотека парсинга
Celery - Реализация очереди


## Предварительный запуск

В проект добавлен selenoid, необходимо предварительно скачать контейнеры с браузерами.

Находясь в директории проекта на одном уровне с файлом `prepare_browsers.bash` выполнить команду `sh prepare_browsers.bash`.

Заполнить файлы переменных окружения своими параметрами!
.env - корневая дирректория, основные настройки бекенда
.env - frontend/.env основные настройки фронтенда

Находясь в директории проекта на одном уровне с файлом `docker-compose.local.yml` запустить `docker-compose -f docker-compose.local.yml up`

Фронтенд доступен на: http://localhost:8080/
Бекенд: http://localhost:8000/

```
Пример файла переменных окружения local.env (файл переменных окружения)
DJANGO_SETTINGS_MODULE=trading.settings
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
DJANGO_ADMINISTRATOR_PASS=adminpass```