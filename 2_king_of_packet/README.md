# King of the Packet

Browsing to http://car, we see the following message.

## Prompt

```
Welcome to King of the Packet 0x1337
--------------------------------------------------------------------------------
We found out that a hacker tried to steal our car. We noticed her capturing our
traffic. Management wants an assessment. I think we are safe. We run the car 
engine server on a secret IP address and UDP port. Even after that the hacker
would need to figure out the password. And even they do, they still wont know
how to control the car because we dont publish the commands to drive the car
--------------------------------------------------------------------------------
The hacker got frustrated and quit but left her capture on the target.
We need you to investigate and figure out if you can take over the car.
--------------------------------------------------------------------------------
The hacker left a note that we think may help.
capture.pcapng holds all the secrets, I think.
--------------------------------------------------------------------------------
One of our techs reminded us that tshark might be useful in extracting info.
You can use it to filter fields like the ip address, port, and data of a capture
Fields that might be useful are ip.src, ip.sport, ip.dst, ip.dport, data.data
The following tshark command will show the ip source, udp port, and data

tshark -r capture.pcapng -T fields -e ip.src -e udp.srcport -e data.data

One other note, data.data is encoded in hexadecimal. You will need to decode it.
For example, try using the command unhex 476f696e6720666f7277617264730a
--------------------------------------------------------------------------------
After determining the ip address and port, connect using netcat. You
can connect using nc -u IP PORT. But replace IP and PORT with the correct values
```

## Solution

Running the provided command, we are provided with the following response.

```
tshark -r capture.pcapng -T fields -e ip.src -e udp.srcport -e data.data

10.3.141.1      31337   506c656173652073656e64207468652070617373776f72642066697273740a
10.3.141.224    47124   726f6f740a
10.3.141.224    47124   70617373776f72640a
10.3.141.224    47124   61646d696e0a
10.3.141.1      31337   41757468656e7469636174696f6e205375636365737366756c0a
10.3.141.224    47124   770a
10.3.141.1      46102   5b42726f6164636173745d20436172206973206d6f76696e6720666f7277617264
10.3.141.1      57798   5b42726f6164636173745d204361722069732073746f7070696e67
10.3.141.1      31337   476f696e6720666f7277617264730a
10.3.141.224    47124   770a
10.3.141.1      35710   5b42726f6164636173745d20436172206973206d6f76696e6720666f7277617264
10.3.141.1      49285   5b42726f6164636173745d204361722069732073746f7070696e67
10.3.141.1      31337   476f696e6720666f7277617264730a
10.3.141.224    47124   780a
10.3.141.1      47286   5b42726f6164636173745d204361722069732073746f7070696e67
10.3.141.1      31337   496e76616c696420636f6d6d616e642e0a
10.3.141.224    47124   730a
10.3.141.1      31337   476f696e67206261636b77617264730a
10.3.141.1      53190   5b42726f6164636173745d20436172206973206d6f76696e67206261636b77617264
10.3.141.1      33548   5b42726f6164636173745d204361722069732073746f7070696e67
10.3.141.224    47124   610a
10.3.141.1      31337   5475726e696e67206c6566740a
10.3.141.1      42410   5b42726f6164636173745d20436172206973206d6f76696e67206c656674
10.3.141.224    47124   640a
10.3.141.1      40111   5b42726f6164636173745d20436172206973206d6f76696e67207269676874
10.3.141.1      60215   5b42726f6164636173745d204361722069732073746f7070696e67
````

We see that the first message is sent from IP ``10.3.141.1`` and port ``31337``. Let us examine the contents of this message. Since the message is hexadecimal encoded, we will need to return it to ASCII using the ``unhex`` command.

```
unhex 506c656173652073656e64207468652070617373776f72642066697273740a
Please send the password first
```

Examining this we can guess that the message is most likely coming from the car and its asking the user to specify the correct password. However, the users first attempt ``root`` is incorrect. We can pipe all the messages to unhex simultaneous using a file pipe like the following: ``tshark -r capture.pcapng -T fields -e data.data | unhex``

```
Please send the password first
root
password
admin
Authentication Successful
w
[Broadcast] Car is moving forward
[Broadcast] Car is stopping
Going forwards
w
[Broadcast] Car is moving forward
[Broadcast] Car is stopping
Going forwards
x
[Broadcast] Car is stopping
Invalid command.
s
Going backwards
[Broadcast] Car is moving backward
[Broadcast] Car is stopping
a
Turning left
[Broadcast] Car is moving leftd
[Broadcast] Car is moving right
[Broadcast] Car is stopping#
```

Examining this traffic. We can determine that the correct password is ``admin`` since the car allows commands afterwards. We can also map the movement commands to ``[w,a,s,d] for [forward,left,back,right]``

To test this out, connect to the car.

```
nc -u 10.3.141.1 31337
admin
Authentication Successful
w
Going forwards
```

## Prompts

0. Instead of individually examining data, prompt students to use a file pipe ``|`` to pipe the data traffic to ``unhex``. 

1. How can we determine which IP address belongs to the car? The car would be sending authentication information and direction information (e.g. please the password first, car is moving)

2. How can we determine if we got the correct password? In the network capture, the car responds with ``Authentication Successful``. It must be the same when we test.

3. If ``w,a,s`` are ``forward, left,back``, what must be the command for ``right?``. Have students make a guess that right could be ``d`` based on keyboard layout and then test their hypothesis. 

## Helpful Pivots for Students

0. Give the students the source code. There is hidden functionality. You can toggle the lights with ``t`` and cause the car to exercise a ``dance`` routine with ``dance.``

1. Ask students how they could take over other teams cars? They would need to connect the other cars WiFi and then issue the same commands. 



