
import serial
import time
import os

# Switch this to false if debugging on a laptop
READ_FROM_PI = True

class PianoStairs():

    def __init__(self):
        self.NUM_PINS = 6

        # Keep track of the previous values so that we can do smoothing
        self.previnputs = [False] * self.NUM_PINS

        if READ_FROM_PI == True:
            self.ser = serial.Serial('/dev/ttyACM0', 9600)
        letters = ["d", "e", "f", "g", "a", "b"]
        letters = letters[::-1]
        self.piano_notes = ["samples/"+letter+".wav" for letter in letters]

    def piano(self, i):
        os.system("omxplayer -o local " + self.piano_notes[i])

    def run(self):
        # Sleep while we wait for everything to boot up.
        time.sleep(3)

        while True:
            line = ""
            if READ_FROM_PI:
                line = self.ser.readline()
            else:
                line = raw_input()

            # Don't do anything if something weird happened w/ serial communication
            if len(line) < 6:
                continue

            for i in range(self.NUM_PINS):
                curr = line[i] != '0'
                prev = self.previnputs[i]
                if curr and not prev:
                    self.piano(i)
                self.previnputs[i] = curr

if __name__ == "__main__":
    pianoStairs = PianoStairs()
    pianoStairs.run()

