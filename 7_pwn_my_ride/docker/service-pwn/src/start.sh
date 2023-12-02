#!/bin/bash
python3 udpserver.py &

while [ true ]; do
    socat -dd TCP4-LISTEN:1337,fork,reuseaddr EXEC:'./car',pty,echo=0,raw,iexten=0 2> /dev/null
    done;

