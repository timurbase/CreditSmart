web: python manage.py migrate --noinput && python manage.py load_banks --noinput && python manage.py collectstatic --noinput && gunicorn creditsmart.wsgi --bind 0.0.0.0:$PORT --workers 2 --log-file -
