#!/bin/bash
git checkout master
git pull origin master
python3 manage.py migrate
python3 manage.py compilemessages
gunicorn --bind 0.0.0.0:80 alfisviewer.wsgi