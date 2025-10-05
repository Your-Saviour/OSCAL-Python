#!/bin/bash
docker compose stop
echo "Stopped"
docker compose rm -f
echo "Removed"
docker compose up --build --force-recreate -d
echo "Restarted"
sleep 1s