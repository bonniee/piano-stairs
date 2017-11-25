"""
Code to be run on a Raspberry Pi.
Plays piano notes based on serial input.

Expects each serial line to be of the form:
cdefgabc

...where each character is either 0 or 1, with no
spaces or spacers in between.

This code expects 8 inputs; if you're e.g. running on
an Arduino Uno and only have 6 inputs, then you should change
NUM_PINS below as well as the letters array to point to
the appropriate sample files.
"""

import serial
import time
import os

DEBUG = False

class PianoStairs():

  def __init__(self):
    self.NUM_PINS = 8

    # Keep track of the previous values so that we can do smoothing
    self.previnputs = [False] * self.NUM_PINS

    if not DEBUG:
      self.ser = serial.Serial('/dev/ttyACM0', 9600, timeout=1)
    letters = ["c1", "d", "e", "f", "g", "a", "b", "c"]

    # remove this line if you plugged the sensors in top-to-bottom ;)
    letters = letters[::-1]

    self.piano_notes = ["samples/"+letter+".wav" for letter in letters]

  def piano(self, i):
    if DEBUG:
      print "Debug Piano: ", i
    else:
      # This assumes you're running on a Raspberry Pi with omxplayer installed.
      # Replace with appropriate system call to play a .wav file if not.
      os.system("omxplayer -o local " + self.piano_notes[i])

  def run(self):
    # Sleep while we wait for everything to boot up.
    time.sleep(3)

    while True:
      line = ""

      if DEBUG:
        line = raw_input()
      else:
        line = self.ser.readline()

      # Don't do anything if something weird happened w/ serial communication
      if len(line) < 8:
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

