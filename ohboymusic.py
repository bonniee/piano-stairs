import pygame

import serial
import time

onpi = True

pygame.mixer.pre_init(channels=6, buffer=1024)
pygame.mixer.init()

class PianoStairs():

    def __init__(self):
        self.numpins = 6
        # switch between piano and guitar every 3 minutes
        self.seconds = 3 * 60

        self.previnputs = [False] * self.numpins

        if onpi == True:
            self.ser = serial.Serial('/dev/ttyACM0', 9600)
        letters = ["d", "e", "f", "g", "a", "b"]
        letters = letters[::-1]
        self.piano_notes = [pygame.mixer.Sound("piano-notes/"+letter+".wav") for letter in letters]
        guit_let = ["e", "a", "d", "g", "b", "e2"]
        self.guitar_notes = [pygame.mixer.Sound("guitar/"+letter+".wav") for letter in guit_let]

    def piano(self, i):
        self.piano_notes[i].play()

    def guitar(self, i):
        self.guitar_notes[i].play()

    def run(self):
        count = 0
        playguit = False

        time.sleep(3)

        while True:
            count += 1
            if count % (20 * self.seconds) == 0:
                playguit = not playguit
            line = ""
            if onpi:
                line = self.ser.readline()
            else:
                line = raw_input()
            if len(line) < 6:
                continue

            for i in range(self.numpins):
                curr = line[i] != '0'
                prev = self.previnputs[i]
                if curr and not prev:
                    if playguit:
                        self.guitar(i)
                    else:
                        self.piano(i)
                self.previnputs[i] = curr

if __name__ == "__main__":
    pianoStairs = PianoStairs()
    pianoStairs.run()

