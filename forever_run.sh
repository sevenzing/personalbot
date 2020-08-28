#!/bin/bash

result=starting_code
time_start=$(($(date +%s%N)/1000000000)) # IN SECONDS 

while [ ${result} != 0 ]; do
    if [ ${result} == 44 ]
    then
        amount_to_sleep=15
        echo "Sleep in ${amount_to_sleep} seconds"
        sleep ${amount_to_sleep}
        time_start=${time_finished}
    fi
    echo "Got exit code ${result}."
    echo "Stop all containers"
    docker-compose down
    echo "Recreating containers"
    docker-compose up -d mongo mongo-express redis

    time_start=${time_finished}
    docker-compose up --build --exit-code-from bot bot

    result=$?
    time_finished=$(($(date +%s%N)/1000000000)) # IN SECONDS 
done

echo "Done. Stop all containers"
docker-compose down
exit $result
