import pygame

import serial
import time

onpi = True

numpins = 6

# switch between piano and guitar every 3 minutes
seconds = 3 * 60

previnputs = [False] * numpins

if onpi:
    ser = serial.Serial('/dev/ttyACM0', 9600)

pygame.mixer.pre_init(channels=6, buffer=1024)
pygame.mixer.init()

# 1 2 3   5 6    8
# g a b c d e f# g
# g a b   d e    g
# c d e f g a b  c
# 8 6 5 3 2 1
letters = ["d", "e", "f", "g", "a", "b"]
letters = letters[::-1]
piano_notes = [pygame.mixer.Sound("piano-notes/"+letter+".wav") for letter in letters]
guit_let = ["e", "a", "d", "g", "b", "e2"]
guitar_notes = [pygame.mixer.Sound("guitar/"+letter+".wav") for letter in guit_let]



def piano(i):
    piano_notes[i].play()

def guitar(i):
    guitar_notes[i].play()

count = 0
playguit = False

time.sleep(3)

while True:
    count += 1
    if count % (20 * seconds) == 0:
        playguit = not playguit
    line = ""
    if onpi:
        line = ser.readline()
    else:
        line = raw_input()
    if len(line) < 6:
        continue

    for i in range(numpins):
        curr = line[i] != '0'
        prev = previnputs[i]
        if curr and not prev:
            if playguit:
                guitar(i)
            else:
                piano(i)
        previnputs[i] = curr

