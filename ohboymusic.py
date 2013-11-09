import pygame

import serial
import time

onpi = True

numpins = 6

# switch between piano and guitar every 3 minutes
seconds = 3 * 60

previnputs = [False for a in range(0, numpins)]

if onpi:
    ser = serial.Serial('/dev/ttyACMO', 9600)

pygame.mixer.pre_init(channels=6, buffer=1024)
pygame.mixer.init()

letters = ["a", "b", "c", "d", "e", "f"]
piano_notes = [pygame.mixer.Sound("notes/"+letter+".wav") for letter in letters]
guit_let = ["e", "a", "d", "g", "b", "e2"]
guitar_notes = [pygame.mixer.Sound("guitar/"+letter+".wav") for letter in guit_let]

def piano(i):
    piano_notes[i].play()

def guitar(i):
    guitar_notes[i].play()

count = 0
playguit = False

while True:
    count += 1
    if count % (20 * seconds) == 0:
        playguit = not playguit
    line = ""
    if onpi:
        line = ser.readline()
    else:
        line = raw_input()
    for i in range(0, numpins):
        curr = line[i] != '0'
        prev = previnputs[i]
        if curr and not prev:
            if playguit:
                guitar(i)
            else:
                piano(i)
        previnputs[i] = curr