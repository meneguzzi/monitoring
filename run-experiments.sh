#!/usr/bin/env bash

git pull

export PYTHONPATH=.

~/slackMessage.sh -m "Started monitoring simulation at `hostname`"

STARTTIME=$(date +%s)

(python gp/gp.py 1 ; python gp/gp.py 2) &
(python gp/gp.py 3 ; python gp/gp.py 4) &
(python gp/gp.py 5 ; python gp/gp.py 6) &
(python gp/gp.py 7 ; python gp/gp.py 8) &
(python gp/gp.py 9 ; python gp/gp.py 10)

ENDTIME=$(date +%s)

~/slackMessage.sh -m "Finished monitoring simulation in $(($ENDTIME - $STARTTIME)) seconds"