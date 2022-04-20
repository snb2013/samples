#!/bin/sh
echo Wait for services
sleep 5

python3 manage.py seed questions.json
