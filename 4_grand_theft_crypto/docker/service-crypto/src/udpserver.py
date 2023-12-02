import socket
import select
import sys
import time
from signal import *
import my_i2c


def broadcast(msg):
    b_sock = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
    b_sock.setsockopt(socket.SOL_SOCKET, socket.SO_BROADCAST, 1)
    b_sock.setsockopt(socket.SOL_SOCKET, socket.SO_BINDTODEVICE, b'wlan0\0')
    server_address = ('255.255.255.255', 2022)
    msg = "[Broadcast] " + msg
    b_msg = bytes(msg, 'ascii')
    b_sock.sendto(b_msg, server_address)

# Termination signal handler - makes sure motor is turned off


def clean(*args):
    print('Cleaning up GPIO')
    sys.exit(0)


for sig in (SIGABRT, SIGILL, SIGINT, SIGSEGV, SIGTERM, SIGQUIT, SIGTSTP):
    signal(sig, clean)

# Decryption
SECRET_KEY = open('SECRET_KEY', 'rb').read()


def decrypt(b1, b2=SECRET_KEY):  # use xor for bytes
    result = bytearray()
    for b1, b2 in zip(b1, b2):
        result.append(b1 ^ b2)
    return bytes(result)


class WifiCar:
    # Constructor - Need a tuple with 4 GPIO pin numbers: (ENA, ENB, IN1, IN3)
    def __init__(self):
        self._epoll = select.epoll()
        self.client_socks = {}
        self.i2c_bus = my_i2c.make_bus()
        self.lights = False
        # Testing lowering the motor speed
        my_i2c.motor_slow(self.i2c_bus)

    def initialize_udpserver(self, port=33047):
        self.serversocket = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
        self.serversocket.bind(('0.0.0.0', port))
        #self.serversocket.bind(('127.0.0.1', port))
        # Register the socket
        self._epoll.register(self.serversocket, select.EPOLLIN)

    # Begin defining directions
    def backward(self):
        my_i2c.backward(self.i2c_bus)
        time.sleep(1)
        broadcast("Car is moving backward")
        self.stop()

    def forward(self):
        my_i2c.forward(self.i2c_bus)
        time.sleep(1)
        broadcast("Car is moving forward")
        self.stop()

    def left(self):
        my_i2c.turn_left(self.i2c_bus)
        time.sleep(0.55)
        broadcast("Car is moving left")
        self.stop()

    def right(self):
        my_i2c.turn_right(self.i2c_bus)
        time.sleep(0.55)
        broadcast("Car is moving right")
        self.stop()

    def stop(self):
        broadcast("Car is stopping")
        my_i2c.stop(self.i2c_bus)
        time.sleep(0.1)

    # Toggle car headlights
    def toggle_lights(self):
        if self.lights == True:
            broadcast("Someone found the light switch")
            my_i2c.lights_off(self.i2c_bus)
            self.lights = False
        else:
            my_i2c.lights_on(self.i2c_bus)
            self.lights = True

    def runserver(self, callback, timeout=1):
        events = self._epoll.poll(timeout)
        for fileno, event in events:

            # receiving input from client
            if event & select.EPOLLIN:
                content, addr = self.serversocket.recvfrom(
                    1024, socket.MSG_DONTWAIT)
                if not content or not content.strip():
                    break
                else:
                    callback(self.serversocket, addr, content.strip())


# create car object
car = WifiCar()
FLAG = True
# define our socket callback


def udp_socket_callback(sock, client, ciphertext):
    print(f"Received command {ciphertext} from {client}")
    msg = decrypt(ciphertext)
    #print(msg, len(msg))
    if msg == b'u':
        car.forward()
        sock.sendto(b'Going forwards\n', client)
    elif msg == b'd':
        sock.sendto(b"Going backwards\n", client)
        car.backward()
    elif msg == b'l':
        sock.sendto(b"Turning left\n", client)
        car.left()
    elif msg == b'r':
        sock.sendto(b"Turning right\n", client)
        car.right()
    elif msg == b't':
        car.toggle_lights()
    else:
        car.stop()
        if msg == b'q':
            sock.sendto(b'Shutting down Command (obsolete)\n', client)
            #global FLAG
            #FLAG = False
        else:
            sock.sendto(b'Platform stopped\n', client)


car.initialize_udpserver()
car.runserver(udp_socket_callback)


# Keyboard testing
print('Use arrow keys to move or press esc to terminate')
while FLAG:
    car.runserver(udp_socket_callback)
