#!/usr/bin/env bash

export PYTHONPATH=.

echo "### Started monitoring simulation ###"

STARTTIME=$(date +%s)

(python2.7 gp/gp.py barter-world 1 ; python2.7 gp/gp.py barter-world 2) &
(python2.7 gp/gp.py barter-world 3 ; python2.7 gp/gp.py barter-world 4) &
(python2.7 gp/gp.py barter-world 5)

ENDTIME=$(date +%s)

echo "Finished monitoring simulation in $(( ($ENDTIME - $STARTTIME)/60 )) minutes"
