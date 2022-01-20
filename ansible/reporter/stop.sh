#!/usr/bin/bash
if ps ax | grep -q "[m]ain.py"; then
pkill -f main.py
while ps ax | grep -q "[m]ain.py";
do
   continue
done
else
echo "not running"
fi
