#!/bin/bash

echo "Stop all containers"
docker-compose down
echo "Building containers"
docker-compose build
echo "Creating database containers"
docker-compose up -d mongo redis
if [ $1 == "--mongo-express" ]; then 
    echo "Creating mongo-express container"
    docker-compose up -d mongo-express
fi

result=starting_code
time_start=$(date +%s) # IN SECONDS 

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

    time_start=${time_finished}
    docker-compose stop bot
    docker-compose up --exit-code-from bot bot

    result=$?
    time_finished=$(date +%s) # IN SECONDS 
done

echo "Done. Stop all containers"
docker-compose down
exit $result
