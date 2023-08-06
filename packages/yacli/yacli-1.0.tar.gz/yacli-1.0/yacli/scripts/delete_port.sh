#!/bin/bash

regex="LISTEN *([0-9]*).*"

RES=$(netstat -luptn 2>&1  | grep $1)
COUNT=$(netstat -luptn 2>&1| grep $1 | wc -l)

if [ $COUNT -ge 2 ]; then
    echo "Too many pid found!"
    exit 0
fi

if [[ $RES =~ $regex ]]; then
    pid=${BASH_REMATCH[1]}
    kill -9 $pid
    echo "Pid ($pid) killed"
else
    echo "No pid found for this port ($1)"
    exit 0
fi
