import pygame
# import RPi.GPIO as GPIO
import time

# GPIO.setmode(GPIO.BCM)
pinnums = [17]
previnputs = [False for a in pinnums]

updownnum = 30
fadeouttime = 500

# for i in pinnums:
	# GPIO.setup(i,GPIO.IN)

pygame.mixer.init()

sounds = []
sounds.append(pygame.mixer.Sound("Piano.ff.C3.wav"))

def play(i):
	sounds[i].play(loops=-1)

def stop(i):
	sounds[i].fadeout(fadeouttime)

play(0)
time.sleep(2)
stop(0)

while True:
	# for i in pinnums:
		# reading = GPIO.input(i)
		# # prev = previnputs[i]
		# if prev:
		# 	if reading - prev > updownnum:
		# 		play(i)
		# 	elif prev - reading > updownnum:
		# 		stop(i)
		# previnputs[i] = reading
	time.sleep(0.05)
	print "d"