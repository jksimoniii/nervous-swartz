#!/bin/bash
set -e

if [ "$1" = 'migrate' ]; then
    python manage.py migrate
fi

exec "$@"