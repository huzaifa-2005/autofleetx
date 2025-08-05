web: python manage.py migrate && python manage.py collectstatic --noinput && gunicorn Car_Rental_System.wsgi:application --bind 0.0.0.0:$PORT
release: python manage.py migrate