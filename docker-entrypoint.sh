#!/bin/sh
case "$1" in
 "flask-server")
     python mock_services/app.py 
    ;;
 "tests")
     python -m pytest 
    ;;
  * )
    exec "$@"
    ;;
esac

