import os
import pygame
from pygame.locals import *
import RPi.GPIO as GPIO


mounted = True
sounds = []

os.environ['SDL_VIDEODRIVER'] = 'dummy'
os.environ['DISPLAY'] = ':0'
import pygame
pygame.init()
pygame.display.set_mode((1,1))

freq = 44100    # audio CD quality
bitsize = -16   # unsigned 16 bit
channels = 2    # 1 is mono, 2 is stereo
buffer = 2048   # number of samples (experiment to get right sound)
pygame.mixer.init(freq, bitsize, channels, buffer)

# setting up GPIO
GPIO.setmode(GPIO.BCM)
GPIO.setup(15, GPIO.OUT)
GPIO.output(15, GPIO.LOW)

led = False
def toggle_led(force_led=None):
	global led
	if force_led is None:
		led = not led
	else:
		led = force_led
	if not led:
		GPIO.output(15, GPIO.LOW)
	else:
		GPIO.output(15, GPIO.HIGH)

i = 0
while True:
	i += 1
	if not os.path.ismount('/media/usb0'):
		if mounted:
			print('not mounted')
		mounted = False
		if (i % 10000) == 0: toggle_led()
		continue

	if not mounted:
		print('mounted')
	mounted = True

	toggle_led(True)

	for event in pygame.event.get():
		print(event.type)
		if event.type == KEYDOWN:
			key = event.key - 256
			print(event.key)
			if key >= 1 and key <= 9:
				if pygame.mixer.music.get_busy():
					print("busy")
					continue
				print('playing sound {}'.format(key))
				try:
					pygame.mixer.music.load('/media/usb0/{}.mp3'.format(key))
					pygame.mixer.music.play()
				except:
					print("no file found")

			if key == 0:
				print('stopping')
				pygame.mixer.music.fadeout(3000)
				
