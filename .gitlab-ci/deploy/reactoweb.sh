#!/bin/sh

set -e

if [ "$1" = "setup" ]
then
  true
else
  # Pull the image
  echo "Pulling $CI_REGISTRY_IMAGE:latest"
  docker pull "$CI_REGISTRY_IMAGE:latest"

  # Check if the container is running
  echo "Is a container called \"$CONTAINER_NAME\" running?"
  version=$(docker container ls --filter name="$CONTAINER_NAME" --format "{{.Image}}")
  if [ -n "$version" ]
  then
    echo "Stopping the container"
    docker container stop "$CONTAINER_NAME"
    docker container rm "$CONTAINER_NAME"
  fi

  echo "Starting \"$CONTAINER_NAME\""
  docker container run --name "$CONTAINER_NAME" -d \
      --restart always \
      --add-host "postgresql:172.17.0.1" \
      -p 9002:80 \
      -e DB_ENGINE="$DB_ENGINE" \
      -e DB_NAME="$DB_NAME" \
      -e DB_USER="$DB_USER" \
      -e DB_PASSWORD="$DB_PASSWORD" \
      -e DB_HOST="$DB_HOST" \
      -e DB_PORT="$DB_PORT" \
      "$CI_REGISTRY_IMAGE:latest"
fi
