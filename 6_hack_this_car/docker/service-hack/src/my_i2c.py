import time
from smbus2 import SMBus

I2C_ADDRESS = 0x18
I2C_COMMAND = 0xFF

# Motor
I2C_STOP = 0x210A
I2C_FORWARD = 0x220A
I2C_BACKWARD = 0x230A
I2C_LEFT = 0x240A
I2C_RIGHT = 0x250A

# Motor Speed
I2C_LEFT_SPEED_SLOW  = 0x2605
I2C_LEFT_SPEED_FAST  = 0x260A
I2C_RIGHT_SPEED_SLOW = 0x2705
I2C_RIGHT_SPEED_FAST = 0x270A

# Headlights
I2C_HEADLIGHT_LEFT_OFF  = 0x3600
I2C_HEADLIGHT_LEFT_ON   = 0x3601
I2C_HEADLIGHT_RIGHT_OFF = 0x3700
I2C_HEADLIGHT_RIGHT_ON  = 0x3701


# TODO - Create an I2C_Bus class which inherits from SMBus


# Functions
def make_bus():
	bus = SMBus(1)
	return bus

def motor_fast(i2c_bus):
	i2c_bus.write_word_data(I2C_ADDRESS, I2C_COMMAND, I2C_LEFT_SPEED_FAST)
	time.sleep(0.01)
	i2c_bus.write_word_data(I2C_ADDRESS, I2C_COMMAND, I2C_RIGHT_SPEED_FAST)	
	time.sleep(0.01)

def motor_slow(i2c_bus):
	i2c_bus.write_word_data(I2C_ADDRESS, I2C_COMMAND, I2C_LEFT_SPEED_SLOW)
	time.sleep(0.01)
	i2c_bus.write_word_data(I2C_ADDRESS, I2C_COMMAND, I2C_RIGHT_SPEED_SLOW)
	time.sleep(0.01)

def turn_right(i2c_bus):
	i2c_bus.write_word_data(I2C_ADDRESS, I2C_COMMAND, I2C_RIGHT)

def turn_left(i2c_bus):
	i2c_bus.write_word_data(I2C_ADDRESS, I2C_COMMAND, I2C_LEFT)

def forward(i2c_bus):
        i2c_bus.write_word_data(I2C_ADDRESS, I2C_COMMAND, I2C_FORWARD)

def backward(i2c_bus):
        i2c_bus.write_word_data(I2C_ADDRESS, I2C_COMMAND, I2C_BACKWARD)

def stop(i2c_bus):
        i2c_bus.write_word_data(I2C_ADDRESS, I2C_COMMAND, I2C_STOP)


def lights_on(i2c_bus):
        i2c_bus.write_word_data(I2C_ADDRESS, I2C_COMMAND, I2C_HEADLIGHT_LEFT_ON)
        time.sleep(0.01)
        i2c_bus.write_word_data(I2C_ADDRESS, I2C_COMMAND, I2C_HEADLIGHT_RIGHT_ON)

def lights_off(i2c_bus):
        i2c_bus.write_word_data(I2C_ADDRESS, I2C_COMMAND, I2C_HEADLIGHT_LEFT_OFF)
        time.sleep(0.01)
        i2c_bus.write_word_data(I2C_ADDRESS, I2C_COMMAND, I2C_HEADLIGHT_RIGHT_OFF)
