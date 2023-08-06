#!/bin/bash

re='^[0-9]+$'

NBR=1
CMD="tail -n 70"

for var in $@; do
    if [[ $var =~ $re ]]; then
        NBR=$var
    else
        CMD=$1
    fi
done


ssh yada.server.citobi.be "cd /srv/tomcat/yada/temp/; ls -1t  | head -$NBR | tail -1 | xargs $CMD"

