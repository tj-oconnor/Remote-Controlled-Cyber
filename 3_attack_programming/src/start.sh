#!/bin/bash

# Remove old container if it still exists
docker rm pin-chal

echo "Creating docker container..."
docker run --device /dev/snd --name pin-chal -it -d attack-programming

echo "Starting ttyd server..."
ttyd.arm ./ttyd.init

echo "Removing old container..."
docker stop pin-chal
docker rm pin-chal

echo "Done"
