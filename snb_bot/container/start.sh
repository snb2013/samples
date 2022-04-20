#!/bin/sh
echo Wait for services
sleep 5

echo Prepare application
python3 manage.py migrate
python3 manage.py loaddata initial_data
python3 manage.py collectstatic --noinput

echo Starting gunicorn
exec gunicorn chatbot.wsgi:application --name chatbot --bind 0.0.0.0:8000
