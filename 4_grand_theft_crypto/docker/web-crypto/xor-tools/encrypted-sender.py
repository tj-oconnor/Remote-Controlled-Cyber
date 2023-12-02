from pwn import *

HOST = '127.0.0.1'
port = 33047

try:
    key = -1

    while (key < 0):
        try:
            key = int(input("Enter the key (in decimal) >>> "))
        except KeyboardInterrupt:
            print("Keyboard interrupt detected. Shutting down...")
            exit()
        except:
            log.info('\tPlease enter a decimal value.')

    while (True):
        msg = ''
        while (msg not in ['u', 'd', 'l', 'r', 't']):
            log.info('\tValid Commands are u,d,l,r,t.')
            msg = input("Enter a valid command >>> ").lower().strip('\n')

        msg = msg.encode()
        result = xor(key, msg)
        p = remote(HOST, port, typ='udp')
        p.sendline(result)
        log.info('Sent Encrypted Command: XOR(%i,%s)' % (key, msg.decode()))
        ans = input('Send Another Command (y|n) >>> ').lower().strip('\n')
        p.close()
        if ans != 'y':
            log.info('Program Terminating. Goodbye')
            break


except KeyboardInterrupt:
    # Handle keyboard interrupt separately
    print("Keyboard interrupt detected. Shutting down...")
