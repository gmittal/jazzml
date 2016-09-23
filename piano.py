from __future__ import division
import os, math
from random import randint
import numpy as np
from music21 import *
from mingus.containers import Note
from mingus.midi import fluidsynth
import simplejson as json
import time

fluidsynth.init(os.getcwd() + "/soundfonts/piano.sf2")

bpm = 240
noteFrequencies = []
noteNamesWithSharps = ["C", "C#", "D", "D#", "E", "E#", "F#", "G", "G#", "A", "A#", "B"]
noteNamesWithFlats = ["C", "Db", "D", "Eb", "Fb", "F", "Gb", "G", "Ab", "A", "Bb", "Cb"]
referenceFrequency = 130.81278265*4 # C

for i in range(0, 12):
    noteFrequencies.append(referenceFrequency*math.pow(2, i/12))

def getChordTones(chordSymbol):
    return eval(os.popen('./util/chordScale "'+chordSymbol+'"').read())

def getImprovScale(quality, symbol):
    scaleType = scale.DorianScale()
    if quality == 1:
        scaleType = scale.MajorScale()
    elif quality == 3:
        scaleType = scale.MixolydianScale()
    tones = getChordTones(symbol)
    for t in range(0, len(tones)):
        tones[t] = tones[t].replace('b', '-')
    scales = scaleType.derive(tones)
    allPitches = scales.getPitches()
    allNoteNames = [i.name for i in allPitches]
    for n in range(0, len(allNoteNames)):
        allNoteNames[n] = allNoteNames[n].replace("-", "b")
    return {'name': scales.name, 'scale': allNoteNames}

def mapFreq(note):
    freq = 800
    if (note in noteNamesWithSharps):
        freq = noteFrequencies[noteNamesWithSharps.index(note)]
    else:
        freq = noteFrequencies[noteNamesWithFlats.index(note)]
    return freq

def playNote(note, beats):
    seconds = beats*60/bpm
    n = Note(note+"-5")
    fluidsynth.play_Note(n)
    time.sleep(seconds);
    fluidsynth.stop_Note(n)
    # freq = mapFreq(note)
    # s = sig(freq, seconds)
    # play(s)
playNote("D", 0.5)
playNote("E", 0.5)
playNote("F", 0.5)
playNote("G", 0.5)
playNote("E", 1)
playNote("C", 0.5)
playNote("D", 0.5)
playNote("E", 0.5)
playNote("F", 0.5)
playNote("G", 0.5)
playNote("E", 1)
playNote("C", 0.5)
playNote("D", 0.5)
playNote("E", 0.5)
playNote("F", 0.5)
playNote("G", 0.5)
playNote("E", 1)
playNote("C", 0.5)
playNote("D", 2)

f = open(os.getcwd()+"/data/currentChord.txt", "r").read()
q = f.split(" ")[1]
c = f.split(" ")[0]
s = getImprovScale(q, c)["scale"]
