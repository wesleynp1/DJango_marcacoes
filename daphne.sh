#!/bin/sh
#se alterar algum aruivo static use: python manage.py collectstatic --clear --noinput
daphne -b 0.0.0.0 -p 8000 wnp_exe.asgi:application