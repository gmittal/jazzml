from __future__ import division
import os, math, time, numpy as np, simplejson as json
from random import randint
from music21 import *
from mingus.containers import Note
from mingus.midi import fluidsynth
import sample as lstm

fluidsynth.init(os.getcwd() + "/soundfonts/piano.sf2")
noteNamesWithSharps = ["C", "C#", "D", "D#", "E", "E#", "F#", "G", "G#", "A", "A#", "B"]
noteNamesWithFlats = ["C", "Db", "D", "Eb", "Fb", "F", "Gb", "G", "Ab", "A", "Bb", "Cb"]
referenceFrequency = 130.81278265*4 # C4
noteFrequencies = [referenceFrequency*math.pow(2, i/12) for i in range(0, 12)]

class Player(object):
    def __init__(self, bpm=120):
        self.lastNotePlayed = None
        self.noteQueue = lstm.sample(40, 1)

    def setBPM(self, bpm):
        self.bpm = bpm

    def sample(self):
        if len(self.noteQueue) == 0:
            self.noteQueue.extend(lstm.sample(40, 1))
        next_note = self.noteQueue[0]
        self.noteQueue = self.noteQueue[1:] # shift the first element
        return next_note

    # Play one note over a particular scale
    def play(self, scale):
        note = self.sample()
        playNote(s[int(note[0])], note[1], scale)

    def playNote(self, note, beats, scale):
        seconds = beats*60/bpm
        if scale == None:
            n = Note(note+"-5")
            fluidsynth.play_Note(n)
            time.sleep(seconds);
            fluidsynth.stop_Note(n)
        else:
            lastIndex = scale.index(lastNotePlayed)
            currentIndex = scale.index(note)
            if (currentIndex > lastIndex):
                n = Note(note+"-6")
                fluidsynth.play_Note(n)
                time.sleep(seconds);
                fluidsynth.stop_Note(n)
            else:
                playNote(note, beats, None)
        self.lastNotePlayed = note

    def getModelLoss():
        return lstm.loss_val

# Given a note name, return a reference frequency
def noteToFreq(note):
    return noteFrequencies[noteNamesWithSharps.index(note)] if note in noteNamesWithSharps else noteFrequencies[noteNamesWithFlats.index(note)]
