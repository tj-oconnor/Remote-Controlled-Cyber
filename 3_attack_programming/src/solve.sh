#!/bin/bash
for i in {0000..9999}
do
    echo "Trying pin: $i"
    if [[ $(./pin $i) != *"Incorrect"* ]]
    then
        echo "Pin found: $i"
	break
    fi
done
