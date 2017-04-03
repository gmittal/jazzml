# Joey Alexander
# Built by Gautam Mittal (2017)
# Real-time chord detection and improvisation software that uses Fast Fourier Transforms, DSP, and machine learning

import sys
sys.path.append('util')
from PyQt4 import QtGui, QtCore
from matplotlib.backends.backend_qt4agg import FigureCanvasQTAgg as FigureCanvas
from matplotlib.backends.backend_qt4agg import NavigationToolbar2QT as NavigationToolbar
from music21 import *
import os, threading, subprocess, numpy as np, atexit, pyaudio, matplotlib.pyplot as plt, chords, peakutils#, piano

global CURRENT_CHORD
chordFinder = chords.ChordDetector()
chordQualities = chords.qualities
chordRoots = chords.noteNames

# Given chord symbol return list of 1, 3, 5, 7 scale degrees ("chord tones")
def chordTones(chordSymbol):
    return eval(os.popen('./util/chordScale "'+chordSymbol+'"').read())

# Given a chord, find an appropriate scale to use for improvisation
def improvisationScale(chord, symbol):
    # Decide on scale type based on common chord-scale conventions
    scaleType = scale.DorianScale()
    if chord.quality == 1:
        scaleType = scale.MajorScale()
    elif chord.quality == 3:
        scaleType = scale.MixolydianScale()

    tones = map(lambda x: x.replace('b', '-'), chordTones(symbol))
    scales = scaleType.derive(tones) # Find the scale based on the given tones
    allPitches = scales.getPitches() # Get the assosciated scale degrees
    allNoteNames = [i.name for i in allPitches] # Turn them into real note names
    return {'name': scales.name, 'scale': allNoteNames}

# Record audio in real-time for chord detection
class MicrophoneRecorder(object):
    def __init__(self, rate=2000, chunksize=2**12):
        self.rate = rate
        self.chunksize = chunksize
        self.p = pyaudio.PyAudio()
        self.stream = self.p.open(format=pyaudio.paInt16,
                                  channels=1,
                                  rate=self.rate,
                                  input=True,
                                  frames_per_buffer=self.chunksize,
                                  stream_callback=self.new_frame)
        self.lock = threading.Lock()
        self.stop = False
        self.frames = []
        atexit.register(self.close)

    def new_frame(self, data, frame_count, time_info, status):
        data = np.fromstring(data, 'int16')
        with self.lock:
            self.frames.append(data)
            if self.stop:
                return None, pyaudio.paComplete
        return None, pyaudio.paContinue

    def get_frames(self):
        with self.lock:
            frames = self.frames
            self.frames = []
            return frames

    def start(self):
        self.stream.start_stream()

    def close(self):
        with self.lock:
            self.stop = True
        self.stream.close()
        self.p.terminate()


class MplFigure(object):
    def __init__(self, parent):
        self.figure = plt.figure(facecolor='white')
        self.canvas = FigureCanvas(self.figure)

class LiveFFTWidget(QtGui.QWidget):
    def __init__(self):
        QtGui.QWidget.__init__(self)
        self.initUI()
        self.initData()
        self.initMplWidget()

    def initUI(self):
        vbox = QtGui.QVBoxLayout()
        self.main_figure = MplFigure(self)
        vbox.addWidget(self.main_figure.canvas)
        self.setLayout(vbox)
        self.setGeometry(300, 300, 350, 300)
        self.setWindowTitle('Joey Alexander')
        self.show()
        timer = QtCore.QTimer()
        timer.timeout.connect(self.handleNewData)
        timer.start(50)
        self.timer = timer

    def initData(self):
        mic = MicrophoneRecorder()
        mic.start()
        self.mic = mic
        self.freq_vect = np.fft.rfftfreq(mic.chunksize,
                                         1./mic.rate)
        self.time_vect = np.arange(mic.chunksize, dtype=np.float32) / mic.rate * 1000


    def initMplWidget(self):
        self.ax_top = self.main_figure.figure.add_subplot(211)
        self.ax_top.set_ylim(-32768, 32768)
        self.ax_top.set_xlim(0, self.time_vect.max())
        self.ax_top.set_xlabel(u'time (ms)', fontsize=6)
        self.ax_bottom = self.main_figure.figure.add_subplot(212)
        self.ax_bottom.set_ylim(0, 1)
        self.ax_bottom.set_xlim(0, self.freq_vect.max())
        self.ax_bottom.set_xlabel(u'frequency (Hz)', fontsize=6)
        self.line_top, = self.ax_top.plot(self.time_vect,
                                         np.ones_like(self.time_vect))
        self.line_bottom, = self.ax_bottom.plot(self.freq_vect,
                                               np.ones_like(self.freq_vect))


    # handles the asynchroneously collected sound chunks
    def handleNewData(self):
        frames = self.mic.get_frames()

        if len(frames) > 0:
            current_frame = frames[-1]

            # get 12x1 chroma vector with respective energies for each note
            chroma = chords.calculateChromagram(self.freq_vect, np.abs(np.fft.rfft(current_frame)))
            chordFinder.detectChord(chroma)

            chordString = ""
            if chordFinder.intervals > 0:
                chordString = str(chordRoots[chordFinder.rootNote]) + str(chordQualities[chordFinder.quality]) + str(chordFinder.intervals)
            else:
                chordString = str(chordRoots[chordFinder.rootNote]) + str(chordQualities[chordFinder.quality])

            improvScale = improvisationScale(chordFinder, chordString)
            CURRENT_CHORD = {
                'chord': chordString,
                'root': chordRoots[chordFinder.rootNote],
                'quality': chordQualities[chordFinder.quality],
                'interval': chordFinder.intervals
            }

            print CURRENT_CHORD

            # plots the time signal
            self.line_top.set_data(self.time_vect, current_frame)

            fft_frame = np.fft.rfft(current_frame)
            fft_frame /= np.abs(fft_frame).max()
            self.line_bottom.set_data(self.freq_vect, np.abs(fft_frame))
            self.main_figure.canvas.draw()


if __name__ == "__main__":
    app = QtGui.QApplication(sys.argv)
    window = LiveFFTWidget()
    sys.exit(app.exec_())
