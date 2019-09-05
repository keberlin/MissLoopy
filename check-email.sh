#!/bin/bash

mllog 10000 | fgrep mlregister | fgrep email | sed -e "s/.*email': u.//" -e "s/., 'ethnicity.*//" | sort -u | python check-email.py
