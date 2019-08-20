#!/bin/bash

mllog 10000 | fgrep mlregister | fgrep email | sed -e "s/.*email': u.//" -e "s/., 'ethnicity.*//" | sort -u | /usr/local/bin/python2.7 check-email.py
