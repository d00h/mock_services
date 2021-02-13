#!/bin/sh
case "$1" in
 "flask-server")
     python mock_services/app.py 
    ;;
 "gunicorn-server")
    gunicorn --workers=4 --bind 0.0.0.0:5000 'mock_services.app:app'
    ;;
 "tests")
     python -m pytest 
    ;;
  * )
    exec "$@"
    ;;
esac

