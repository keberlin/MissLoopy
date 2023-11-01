#!/bin/bash

# get the GeoLite2 db
NAME=GeoLite2-Country-CSV
rm -rf ${NAME}_*
FILE=$NAME.zip
curl "https://download.maxmind.com/app/geoip_download_by_token?edition_id=$NAME&suffix=zip&token=v2.local.qOMdscqpxaWqODxQ77hKWQEKj3xYLRyBH3OBhTrvd4Xf0Pd14bw7zPlgzmAtcSxIXZHfyKe_hqeQXEKyE2WAr56sSEf2ney26ntprvgP6Q8nZQPnr8-Mjnw667E8R4RwTuNx3hhLWsb_Eutb0xWe0u8hD_XCVK6brlvyHKZJKOtlAadpcNC3xkY4rJT3dzHVPpPoqQ" > $FILE
unzip -o $FILE
rm -f $FILE
mv ${NAME}_*/GeoLite2-Country-Blocks-IPv4.csv GeoLite2-Country-Blocks-IPv4.csv
mv ${NAME}_*/GeoLite2-Country-Locations-en.csv GeoLite2-Country-Locations.csv

# get the dbip db
NAME=dbip-country-lite
rm -f $NAME.csv
FILE=$NAME-`date +%Y-%m`.csv
curl http://download.db-ip.com/free/$FILE.gz > $FILE.gz
gunzip -f $FILE.gz
mv $FILE $NAME.csv
