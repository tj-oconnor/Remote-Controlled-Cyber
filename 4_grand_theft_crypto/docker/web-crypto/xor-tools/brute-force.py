from pwn import *
import time

HOST = '127.0.0.1'
port = 33047

p = remote(HOST, port, typ='udp')

log.info("Brute Force Version 1.0")

try:
    min_guess = int(
        input("Enter an integer to start brute forcing at [Hint: 2^0] >>> "))
    max_guess = int(
        input("Enter an integer to stop brute focing at [Hint: 2^8] >>> "))
except:
    log.info('Please try again and enter integers for your input')
    exit()

"Enter the largest decimal value you would like to brute force as the key"

progress_bar = log.progress('Testing integer: ')
for val in range(min_guess, max_guess):
    req = val.to_bytes(1, 'big')
    progress_bar.status('%i (Binary: %s)' % (val, bin(val).replace('0b', '')))
    p.sendline(req)
    time.sleep(0.5)
