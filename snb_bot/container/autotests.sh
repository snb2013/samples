#!/bin/sh
echo Wait for services
sleep 5

python3 manage.py test chatbot.tests
