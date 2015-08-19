#!/bin/bash

./admin.py <<EOF
ALTER SEQUENCE profiles_id_seq RESTART WITH 1
ALTER SEQUENCE photos_pid_seq RESTART WITH 1
EOF
