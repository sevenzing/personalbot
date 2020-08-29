#!/bin/bash

result=starting_code
time_start=$(($(date +%s%N)/1000000000)) # IN SECONDS 

while [ ${result} != 0 ]; do
    echo "Got exit code ${result}."

    if [ ${result} == 44 ]; then
        amount_to_sleep=15
        echo "Sleep in ${amount_to_sleep} seconds"
        sleep ${amount_to_sleep}
        time_start=${time_finished}
    elif [ ${result} == 10 ]; then
        echo "Restart request from the bot"
    else
        echo "Unknown exit code"
    fi

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
