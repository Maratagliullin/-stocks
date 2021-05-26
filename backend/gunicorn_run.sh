#!/bin/bash

set -eEu -o pipefail

python manage.py migrate --noinput

python manage.py shell -c "from django.contrib.auth.models import User; User.objects.filter(is_superuser=True).exists() or User.objects.create_superuser('administrator', 'admin@admin.com', '${DJANGO_ADMINISTRATOR_PASS}');"

python manage.py collectstatic --noinput

#exec gunicorn -w 3 --access-logfile /var/log/gunicorn/access_logs.log --log-level error --error-logfile /var/log/gunicorn/error_logs.log --bind 0.0.0.0:8000 ${DJANGO_WSGI}
exec gunicorn -w 3 --bind 0.0.0.0:8000 ${DJANGO_WSGI}