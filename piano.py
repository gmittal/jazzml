from __future__ import division
import numpy as np
from scikits.audiolab import play

def testsignal(hz,seconds, amplitude = .5,sr=44100.):
    '''
    Create a sine wave at hz for n seconds
    '''
    # cycles per sample
    cps = hz / sr
    # total samples
    ts = seconds * sr
    return amplitude * np.sin(np.arange(0,ts*cps,cps) * (2*np.pi))
