#!/usr/bin/env bash

# Apply database migrations
python manage.py migrate

# Collect static files into STATIC_ROOT
python manage.py collectstatic --noinput
