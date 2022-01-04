#!/bin/bash
python3 manage.py migrate
python3 manage.py compilemessages
gunicorn alfisviewer.wsgi