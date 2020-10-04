#!/usr/bin/env bash

export PYTHONPATH=.

echo "### Started monitoring simulation ###"

STARTTIME=$(date +%s)

echo "Running experiments for BTW domain..."
(python2.7 gp/gp.py tpp 1 ; python2.7 gp/gp.py tpp 2) &
(python2.7 gp/gp.py tpp 3 ; python2.7 gp/gp.py tpp 5) &

echo "Running experiments for BD domain..."
(python2.7 gp/gp.py psr 1 ; python2.7 gp/gp.py psr 2) &
(python2.7 gp/gp.py psr 3 ; python2.7 gp/gp.py psr 4) &
(python2.7 gp/gp.py psr 5)

ENDTIME=$(date +%s)

echo "Finished monitoring simulation in $(( ($ENDTIME - $STARTTIME)/60 )) minutes"
