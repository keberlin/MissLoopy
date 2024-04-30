#!/usr/bin/bash

export LC_ALL=en_US

SCRIPTPATH=`dirname "$0"`

cd $SCRIPTPATH

source venv/bin/activate

export FLASK_DEBUG=1

gunicorn --limit-request-line 0 --workers 1 --threads 1 --timeout 0 --bind :6001 wsgi:app
