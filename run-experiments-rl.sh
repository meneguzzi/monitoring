#!/usr/bin/env bash

export PYTHONPATH=.

echo "### Started monitoring simulation ###"

STARTTIME=$(date +%s)

echo "Running experiments for BTW domain..."
(python2.7 rl/rl.py barter-world 1 ; python2.7 rl/rl.py barter-world 2) &
(python2.7 rl/rl.py barter-world 3 ; python2.7 rl/rl.py barter-world 4) &
(python2.7 rl/rl.py barter-world 5)

echo "Running experiments for BD domain..."
(python2.7 rl/rl.py bridges 1 ; python2.7 rl/rl.py bridges 2) &
(python2.7 rl/rl.py bridges 3 ; python2.7 rl/rl.py bridges 4) &
(python2.7 rl/rl.py bridges 5)

ENDTIME=$(date +%s)

echo "Finished monitoring simulation in $(( ($ENDTIME - $STARTTIME)/60 )) minutes"
