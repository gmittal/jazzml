from __future__ import division
import os, math, time, numpy as np, simplejson as json
from random import randint
from music21 import *
from mingus.containers import Note
from mingus.midi import fluidsynth
import sample as lstm

fluidsynth.init(os.getcwd() + "/soundfonts/piano.sf2")

lastNotePlayed = None
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

def playNote(note, beats, scale):
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

    lastNotePlayed = note


f = open(os.getcwd()+"/data/currentChord.txt", "r").read()
q = f.split(" ")[1]
c = f.split(" ")[0]
s = getImprovScale(q, c)["scale"]
print s
output = lstm.sample(40, 1);

for note in output:
    playNote(s[int(note[0])], note[1], None)
