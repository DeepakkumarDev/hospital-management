web: python manage.py migrate --noinput  && python manage.py create_superuser && python manage.py collectstatic --noinput && gunicorn healthcare.wsgi:application --log-file -
