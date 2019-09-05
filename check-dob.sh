#!/bin/bash

mllog 10000 | fgrep mlregister | fgrep dob | sed -e "s/.*dob': u.//" -e "s/., 'gender.*//" | sort -u | python check-dob.py
