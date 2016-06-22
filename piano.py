from __future__ import division
import math
import numpy as np
from scikits.audiolab import play

bpm = 160
noteFrequencies = []
noteNamesWithSharps = ["C", "C#", "D", "D#", "E", "F", "F#", "G", "G#", "A", "A#", "B"]
noteNamesWithFlats = ["C", "Db", "D", "Eb", "E", "F", "Gb", "G", "Ab", "A", "Bb", "B"]
referenceFrequency = referenceFrequency = 130.81278265*3 # C

for i in range(0, 12):
    noteFrequencies.append(referenceFrequency*math.pow(2, i/12))

def sig(hz,seconds, amplitude = .5,sr=44100.):
    cps = hz / sr
    ts = seconds * sr
    return amplitude * np.sin(np.arange(0,ts*cps,cps) * (2*np.pi))

# sync playNote function using frequency lookup
def playNote(note, beats):
    seconds = beats*60/bpm
    freq = 800
    if (note in noteNamesWithSharps):
        freq = noteFrequencies[noteNamesWithSharps.index(note)]
    else:
        freq = noteFrequencies[noteNamesWithFlats.index(note)]
    s = sig(freq, seconds)
    play(s)

playNote("C", 1/2)
playNote("C#", 1/2)
playNote("D", 1)
playNote("G", 4)
