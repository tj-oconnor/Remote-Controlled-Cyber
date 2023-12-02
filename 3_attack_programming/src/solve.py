#!/usr/bin/python3

from subprocess import check_output as shell

for i in range(0, 10000):
    pin = str(i)
    while len(pin) < 4:
        pin = '0' + pin

    print("Trying pin:", pin)
    if not b'Incorrect' in shell(['./pin', pin]):
        print("Pin found:", pin)
        break
