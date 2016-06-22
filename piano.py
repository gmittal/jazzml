from __future__ import division
import os, math
from random import randint
import numpy as np
from scikits.audiolab import play
from music21 import *

bpm = 300
noteFrequencies = []
noteNamesWithSharps = ["C", "C#", "D", "D#", "E", "E#", "F#", "G", "G#", "A", "A#", "B"]
noteNamesWithFlats = ["C", "Db", "D", "Eb", "Fb", "F", "Gb", "G", "Ab", "A", "Bb", "Cb"]
referenceFrequency = referenceFrequency = 130.81278265*4 # C

for i in range(0, 12):
    noteFrequencies.append(referenceFrequency*math.pow(2, i/12))

def getChordTones(chordSymbol):
    return eval(os.popen('./scripts/chordScale "'+chordSymbol+'"').read())

def getImprovScale(quality, symbol):
    scaleType = scale.DorianScale()
    if quality == 1:
        scaleType = scale.MajorScale()
    elif quality == 3:
        scaleType = scale.MixolydianScale()
    tones = getChordTones(symbol)
    for t in range(0, len(tones)):
        tones[t] = tones[t].replace('b', '-')
    # print tones
    scales = scaleType.derive(tones)
    allPitches = scales.getPitches()
    allNoteNames = [i.name for i in allPitches]
    for n in range(0, len(allNoteNames)):
        allNoteNames[n] = allNoteNames[n].replace("-", "b")
    return {'name': scales.name, 'scale': allNoteNames}

def sig(hz,seconds, amplitude = .5,sr=44100.):
    cps = hz / sr
    ts = seconds * sr
    return amplitude * np.sin(np.arange(0,ts*cps,cps) * (2*np.pi))

def mapFreq(note):
    freq = 800
    if (note in noteNamesWithSharps):
        freq = noteFrequencies[noteNamesWithSharps.index(note)]
    else:
        freq = noteFrequencies[noteNamesWithFlats.index(note)]
    return freq

# sync playNote function using frequency lookup
def playNote(note, beats):
    seconds = beats*60/bpm
    freq = mapFreq(note)
    s = sig(freq, seconds)
    play(s)

while True:
    f = open("currentChord.txt", "r").read()
    q = f.split(" ")[1]
    c = f.split(" ")[0]
    s = getImprovScale(q, c)["scale"]
    note = s[randint(0, 7)]
    print c, note, mapFreq(note), s
    playNote(note, 1/2)

# playNote("C", 1/2)
# playNote("C#", 1/2)
# playNote("D", 1)
# playNote("G", 4)
