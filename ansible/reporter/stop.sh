#!/usr/bin/bash
pkill -f main.py
while ps ax | grep -q "[m]ain.py";
do
   continue
done
