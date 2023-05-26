#!/usr/bin/env python

./dinopedia/manage.py migrate

export DJANGO_SUPERUSER_PASSWORD=ADMIN789
./dinopedia/manage.py createsuperuser --no-input --username oji --email oji@protonmail.com

./dinopedia/manage.py runserver 0.0.0.0:8000
