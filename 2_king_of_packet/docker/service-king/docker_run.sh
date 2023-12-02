#!/bin/bash
docker run --device /dev/i2c-1 --network host --restart always -d -it cocoa1
