# Prompt

To prevent further ``hacking``, the car is now running an encrypted connection on UDP port 33047. It uses a one-time pad (XOR) to encrypt traffic. The key is a full 8-bits in length. So there is no way to crack it, or is there?

# Solution

Since it only uses a single byte key, we know the key can range from ``bytes([0])`` to ``bytes([255])``. From previous experience, we know that the potential inputs are ``u,d,l,r,t`` to move ``u``p, ``d``own, ``l``eft, ``r``ight, or ``t``oggle the lights. 

We can try several different approaches to solve this. One method may be to send ``bytes([0])`` to ``bytes([255])`` one byte at a time and try to observe that cars behaivor.


```python
from pwn import *
import time

HOST = '192.168.1.158'
port = 33047

p = remote(HOST,port,typ='udp')

for val in range(0,255):
   req = bytes([val])
   log.info('Testing bytes: %s (%i)' %(req,val))
   p.sendline(req)
   time.sleep(0.5)
```

Observing this, youll most likely notice that on ``req == b'\xc2'``, the car moves ``u``p. We can use this to determine the key.

```python
behavior = b'u'
send_bytes = b'\xc2'
key = xor(behavior,send_bytes)
log.info('Discovered Key: %s' %key)
```

We can then use this knowledge ``'Discovered Key: b'\xb7'`` to control the car

```python
from pwn import *
import time

HOST = '192.168.1.158'
port = 33047
key = b'\xb7'

p = remote(HOST,port,typ='udp')

konami_code = [b'u', b'u', b'd', b'd', b'l', b'r', b'l', b'r', b't', b't']

for move in konami_code:
    p.sendline(xor(key,move))
    time.sleep(0.5)

```

To make this a little easier on students, we have included a web applicaiton on ``port 7681``. So by browing to http://car_ip:7681, you should see the the following message

```
Welcome to Grand Theft Crypto 0x1337
--------------------------------------------------------------------------------
We found out that a hacker tried to compromise our super secure car.
We use full 8-bit XOR encryption to secure our cars commands.
So the hacker would need to calculate XOR(key,command) to compromise the car.
The valid car commands are 'u','d','l','r','t' to move the car.
But the key is a secret. I think the hacker was trying to figure it out.
--------------------------------------------------------------------------------
The hacker got frustrated and quit but left her tools on the target.
We need you to investigate and figure out if you can take over the car.
--------------------------------------------------------------------------------
The hacker left a note that we think may help.
if xor(a,b)=c then xor(a,c)=b and xor(b,c)=a
--------------------------------------------------------------------------------
The tools she left are:
brute-force.py       : attempts to brute force different byte values to car.
xor-calculator.py    : calculates the xor(value,command).
encrypted-sender.py  : sends encrypted car commands for xor(key,command).
--------------------------------------------------------------------------------
To run any of the tools type python3 followed by the tool name.
Maybe start with the brute force tool by typing python3 brute-force.py
```

You can use this to ``brute-force`` and ``discover the key`` the car.

```
{16:41}/xor-tools ➭ python3 brute-force.py 
[+] Opening connection to 127.0.0.1 on port 33047: Done
[*] Brute Force Version 1.0
Enter an integer to start brute forcing at [Hint: 2^0] >>> 0
Enter an integer to stop brute focing at [Hint: 2^8] >>> 255

[O] Testing integer: : 219 (Binary: 11011111)
```

Brute-forcing we see the car turn ``left`` and ``219``. So lets see if we can figure out the key since xor(encrypted_value,command)==key. So if we xor(219,'l'), the result should be the key.

```
python3 xor-calculator.py
Enter a decimal value to XOR >>> 219
[*]     Valid Commands are u,d,l,r,t.
Enter a valid command >>> l
[*]     Result of XOR(219,l) = b'\xb7'
[*]     b'\xb7' is represented as 183 in decimal.
```

It says the key is now 183. We can test our hypothesis and try to send the command

```
python3 encrypted-sender.py 
Enter the key (in decimal) >>> 183
[*]     Valid Commands are u,d,l,r,t.
Enter a valid command >>> l
[+] Opening connection to 127.0.0.1 on port 33047: Done
[*] Sent Encrypted Command: XOR(183,l)
```

The car moves!

## Helpful Pivots for Students

- If they miss the exact value, they could just brute smaller set. Lets say they know its somewhere between 210 to 225, they could just start the program back up and brute-force between 210 to 225.

- Further, if they cant figure out the key - they could just perform a ``replay attack`` by brute-forcing between 219-220. 

- The key will always be the same for all messages. So if they are getting different keys, they have observed the behavior wrong. Have them test different values and observations, the key should be the same for all values.
