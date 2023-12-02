# RUN AS ROOT
import keyboard, socket, time

#server = ("127.0.0.1", 31337)
server = ("192.168.1.232", 31337)
sock = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)


print('Use arrow keys to move or press esc to terminate')
while True:
	event = keyboard.read_event()
	if event.event_type == keyboard.KEY_DOWN and event.name == 'esc':
		break
	elif event.event_type == keyboard.KEY_DOWN and event.name == 'up':
		msg = b'u'
		sock.sendto(msg, server)
	elif event.event_type == keyboard.KEY_UP and event.name == 'up':
		msg = b's'
		sock.sendto(msg, server)
	elif event.event_type == keyboard.KEY_DOWN and event.name == 'down':
		msg = b'd'
		sock.sendto(msg, server)
	elif event.event_type == keyboard.KEY_UP and event.name == 'down':
		msg = b'stop'
		sock.sendto(msg, server)
	elif event.event_type == keyboard.KEY_DOWN and event.name == 'left':
		msg = b'l'
		sock.sendto(msg, server)
	elif event.event_type == keyboard.KEY_UP and event.name == 'left':
		msg = b'h'
		sock.sendto(msg, server)
	elif event.event_type == keyboard.KEY_DOWN and event.name == 'right':
		msg = b'r'
		sock.sendto(msg, server)
	elif event.event_type == keyboard.KEY_UP and event.name == 'right':
		msg = b'halt'
		sock.sendto(msg, server)
	elif event.event_type == keyboard.KEY_DOWN and event.name == 'q':
		msg = b'q'
		sock.sendto(msg, server)
		break

time.sleep(1)
