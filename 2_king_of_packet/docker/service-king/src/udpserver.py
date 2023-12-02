
#import wiringpi as GPIO
import socket
import select
import sys
import time
from signal import *
import my_i2c
#import keyboard

authenticated_clients = set()


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


class WifiCar:
    # Constructor - Need a tuple with 4 GPIO pin numbers: (ENA, ENB, IN1, IN3)
    def __init__(self):
        self._epoll = select.epoll()
        self.client_socks = {}
        self.i2c_bus = my_i2c.make_bus()
        self.lights = False
        # Testing lowering the motor speed
        my_i2c.motor_fast(self.i2c_bus)

    def initialize_udpserver(self, port=31337):
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

    def spin(self):
        my_i2c.turn_right(self.i2c_bus)
        time.sleep(10)
        broadcast("Car is spinning")
        self.stop()

    def dance(self):
        for i in range(4):
            my_i2c.forward(self.i2c_bus)
            time.sleep(1)
            my_i2c.backward(self.i2c_bus)
            time.sleep(1)
            if i == 0:
                my_i2c.turn_right(self.i2c_bus)
                time.sleep(0.55)
            if i == 1:
                my_i2c.turn_left(self.i2c_bus)
                time.sleep(1.1)
            if i == 2:
                my_i2c.turn_right(self.i2c_bus)
                time.sleep(0.55)
        broadcast("Car is spinning")
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


def udp_socket_callback(sock, client, msg):
    print(f"Received command {msg} from {client}")
    if client not in authenticated_clients:
        if msg == b'admin':
            authenticated_clients.add(client)
            sock.sendto(b"Authentication Successful\n", client)
            return
        else:
            sock.sendto(b"Please send the password first\n", client)
            return
    if msg == b'f' or msg == b'w':
        car.forward()
        sock.sendto(b'Going forwards\n', client)
    elif msg == b'b' or msg == b's':
        sock.sendto(b"Going backwards\n", client)
        car.backward()
    elif msg == b'l' or msg == b'a':
        sock.sendto(b"Turning left\n", client)
        car.left()
    elif msg == b'r' or msg == b'd':
        sock.sendto(b"Turning right\n", client)
        car.right()
    elif msg == b't':
        car.toggle_lights()
    elif msg == b'spin':
        sock.sendto(b"Spin cycle...\n", client)
        car.spin()
    elif msg == b'dance':
        sock.sendto(b"Jiggle jiggle\n", client)
        car.dance()
    else:
        car.stop()
        if msg == b'q':
            sock.sendto(b"You've logged out.\n", client)
            authenticated_clients.discard(client)
            #global FLAG
            #FLAG = False
        else:
            sock.sendto(b'Invalid command.\n', client)


car.initialize_udpserver()
car.runserver(udp_socket_callback)


# Keyboard testing
print('Use arrow keys to move or press esc to terminate')
while FLAG:
    car.runserver(udp_socket_callback)
