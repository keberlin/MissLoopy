#!/usr/bin/bash

pg_dump ipaddress > ipaddress.dump
pg_dump gazetteer > gazetteer.dump
pg_dump missloopy > missloopy.dump
