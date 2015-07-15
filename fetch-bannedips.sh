#!/bin/bash

wget http://www.stopforumspam.com/downloads/bannedips.zip
unzip -o bannedips.zip
rm -f bannedips.zip
sed 's/,/\
/g' bannedips.csv > bannedips.txt
