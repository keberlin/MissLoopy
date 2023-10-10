#!/usr/bin/bash

export LC_ALL=en_US

SCRIPTPATH=`dirname "$0"`

cd $SCRIPTPATH

source venv/bin/activate

export FLASK_DEBUG=1

flask run -p 6001
