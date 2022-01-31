#!/usr/bin/bash
set -e
if ! ps ax | grep -q "[m]ain.py"; then
source ./venv/bin/activate
nohup python3 ./main.py -p $1 -o $2  <&- &> ./reporter_process.log &
else
echo "running"
fi
