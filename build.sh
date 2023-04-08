#!/usr/bin/env bash

set -o errexit  # exit on error

python manage.py migrate

python manage.py runserver 0.0.0.0:8000
