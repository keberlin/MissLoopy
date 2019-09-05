#!/bin/bash

JUNK_AUTO=junk-auto.log
JUNK_REPORTED=junk-reported.log
JUNK_TEMP=/tmp/junk.log

# Truncate the log to max 5000 lines
uniq $JUNK_AUTO | tail -5000 > $JUNK_TEMP
cmp -s $JUNK_AUTO $JUNK_TEMP || (mv $JUNK_TEMP $JUNK_AUTO; chmod 666 $JUNK_AUTO)
uniq $JUNK_REPORTED | tail -5000 > $JUNK_TEMP
cmp -s $JUNK_REPORTED $JUNK_TEMP || (mv $JUNK_TEMP $JUNK_REPORTED; chmod 666 $JUNK_REPORTED)
# Analyse its contents and create spam keyword list
python analyse-junk.py $JUNK_AUTO $JUNK_REPORTED
