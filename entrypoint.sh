#!/bin/bash
python3 manage.py migrate
python3 manage.py compilemessages
gunicorn --bind 0.0.0.0:80 alfisviewer.wsgi