#!/bin/bash

cleanup() {
    rm -rf ./php/output
    docker container prune -f
    docker image prune  -f
}
trap cleanup EXIT

# docker compose build --no-cache
# docker compose up -d --force-recreate

docker compose build
docker compose up -d