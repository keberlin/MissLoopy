#!/usr/bin/bash

export LC_ALL=en_US

SCRIPTPATH=`dirname "$0"`

cd $SCRIPTPATH

source venv/bin/activate

gunicorn --limit-request-line 0 --workers 1 --threads 5 --timeout 0 --bind :6000 wsgi:app
