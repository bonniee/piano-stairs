import pygame
import serial
import time

numpins = 6

previnputs = [False for a in range(0, numpins)]
ser = serial.Serial('/dev/ttyACMO', 9600)

fadeouttime = 500

pygame.mixer.init()

letters = ["a", "b", "c", "d", "e", "f"]
sounds = [pygame.mixer.Sound("notes/"+letter+".wav") for letter in letters]

def play(i):
    sounds[i].play(loops=0)

while True:
    line = ser.readline()
    for i in range(0, numpins):
        curr = line[i] != '0'
        prev = previnputs[i]
        if curr and not prev:
            play(i)
        previnputs[i] = curr