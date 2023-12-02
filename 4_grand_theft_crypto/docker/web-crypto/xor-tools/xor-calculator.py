from pwn import *

try:
    key = -1

    while (key < 0):
        try:
            key = int(input("Enter a decimal value to XOR >>> "))
        except KeyboardInterrupt:
            print("Keyboard interrupt detected. Shutting down...")
            exit()
        except:
            log.info('\tPlease enter a decimal value.')

    msg = ''
    while (msg not in ['u', 'd', 'l', 'r', 't']):
        log.info('\tValid Commands are u,d,l,r,t.')
        msg = input("Enter a valid command >>> ").lower().strip('\n')

    msg = msg.encode()
    result = xor(key, msg)

    log.info('\tResult of XOR(%i,%s) = %s' %
             (key, msg.decode(), result))
    log.info('\t%s is represented as %i in decimal.' %
             (result, int(result.hex(), 16)))

except KeyboardInterrupt:
    # Handle keyboard interrupt separately
    print("Keyboard interrupt detected. Shutting down...")
