#!/usr/bin/bash
set -e
if ! ps ax | grep -q "[m]ain.py"; then
source /root/ansible_test/reporter/venv/bin/activate
nohup python3 /root/ansible_test/reporter/main.py -p $1 -o $2  <&- &> my.admin.log.file &
fi