#!/bin/bash

# get the GeoLite2 db
NAME=GeoLite2-Country-CSV
rm -rf ${NAME}_*
FILE=$NAME.zip
wget http://geolite.maxmind.com/download/geoip/database/$FILE
unzip -o $FILE
rm -f $FILE
mv ${NAME}_*/GeoLite2-Country-Blocks-IPv4.csv GeoLite2-Country-Blocks-IPv4.csv
mv ${NAME}_*/GeoLite2-Country-Locations-en.csv GeoLite2-Country-Locations.csv

# get the dbip db
NAME=dbip-country
rm -f $NAME.csv
FILE=$NAME-`date +%Y-%m`.csv
wget http://download.db-ip.com/free/$FILE.gz
gunzip -f $FILE.gz
mv $FILE $NAME.csv
