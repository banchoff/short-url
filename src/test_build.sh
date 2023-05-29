#!/bin/env bash

# Most recent tag
ADMIN="root"
PASS="mypassword"
PORT="8020"
GIT_TAG=`git describe --tags --abbrev=0`
ID=`uuidgen`
DOCKER_NAME="shorturl-$GIT_TAG-$ID"

RED='\033[0;31m'
GREEN='\033[0;32m'
NC='\033[0m'


# Create image
echo "Creating docker image $DOCKER_NAME"
docker build -t "$DOCKER_NAME" . >/dev/null 2>/dev/null
if [ $? -ne 0 ]
then
    echo -e "${RED}Error building $DOCKER_NAME image${NC}"
    exit 1
fi

# Run image
echo "Running container based on $DOCKER_IMAGE"
CONTAINER_ID=`docker run -d -p $PORT:$PORT -e DJANGO_SUPERUSER_USERNAME=$ADMIN -e DJANGO_SUPERUSER_PASSWORD=$PASS -e DJANGO_SUPERUSER_EMAIL=root@example.com -e DJANGO_DEBUG=False "$DOCKER_NAME"`
if [ $? -ne 0 ]
then
    echo "Error running image"
    echo "Deleting image"
    docker rmi "$DOCKER_NAME"
    if [ $? -ne 0 ]
    then
	echo "Error deleting image"
    fi
    exit 2
fi

echo "Running tests on container"

sleep 5

./test_login.sh "$PORT" "$ADMIN" "$PASS"
if [ $? -ne 0 ]
then
    echo -e "${RED}Error testing the app${NC}"
    echo -e "${RED}The app is not running or we cannot log in${NC}"
else
    echo -e "${GREEN}Log in. App running.${NC}"
fi

echo "Halting container"
docker stop "$CONTAINER_ID"
if [ $? -ne 0 ]
then
    echo "Error halting container"
fi

echo "Deleting container"
docker container rm "$CONTAINER_ID"
if [ $? -ne 0 ]
then
    echo "Error deleteing container"
fi

echo "Deleting image"
docker rmi "$DOCKER_NAME"
if [ $? -ne 0 ]
then
    echo "Error deleteing image"
fi
