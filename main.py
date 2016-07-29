import sys, os, threading, subprocess
import atexit
import pyaudio
import numpy as np
import matplotlib.pyplot as plt
from PyQt4 import QtGui, QtCore
from matplotlib.backends.backend_qt4agg import FigureCanvasQTAgg as FigureCanvas
from matplotlib.backends.backend_qt4agg import NavigationToolbar2QT as NavigationToolbar
import chords
from music21 import *
import peakutils

chordFinder = chords.ChordDetector()
chordQualities = ["min", "maj", "sus", "", "-", "+"]
chordRoots = ["C", "Db", "D", "Eb", "E", "F", "Gb", "G", "Ab", "A", "Bb", "B"]

def getChordTones(chordSymbol):
    return eval(os.popen('./util/chordScale "'+chordSymbol+'"').read())

def updateChordFile(symbol, quality):
    f = open("currentChord.txt", "w")
    f.write(symbol)
    f.write(" "+str(quality))
    f.close()

def findObjects(array, value):
    ix = []
    for i in range(0, len(array)):
        if array[i] == value:
            ix.append(i)
    return ix

def getImprovScale(chord, symbol):
    scaleType = scale.DorianScale()
    if chord.quality == 1:
        scaleType = scale.MajorScale()
    elif chord.quality == 3:
        scaleType = scale.MixolydianScale()
    tones = getChordTones(symbol)
    for t in range(0, len(tones)):
        tones[t] = tones[t].replace('b', '-')
    scales = scaleType.derive(tones)
    allPitches = scales.getPitches()
    allNoteNames = [i.name for i in allPitches]
    return {'name': scales.name, 'scale': allNoteNames}

class MicrophoneRecorder(object):
    def __init__(self, rate=2000, chunksize=1024):
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
        self.toolbar = NavigationToolbar(self.canvas, parent)

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


    def handleNewData(self):
        """ handles the asynchroneously collected sound chunks """
        # gets the latest frames
        frames = self.mic.get_frames()

        if len(frames) > 0:
            # keeps only the last frame
            current_frame = frames[-1]

            # get 12x1 chroma vector with respective energies for each note
            chroma = chords.calculateChromagram(self.freq_vect, np.abs(np.fft.rfft(current_frame)))
            chordFinder.detectChord(chroma)

            chordString = ""
            if chordFinder.intervals > 0:
                chordString = str(chordRoots[chordFinder.rootNote]) + str(chordQualities[chordFinder.quality]) + str(chordFinder.intervals)
            else:
                chordString = str(chordRoots[chordFinder.rootNote]) + str(chordQualities[chordFinder.quality])

            improvScale = getImprovScale(chordFinder, chordString)
            updateChordFile(chordString, chordFinder.quality)

            # plots the time signal
            self.line_top.set_data(self.time_vect, current_frame)

            # computes and plots the fft signal
            fft_frame = np.fft.rfft(current_frame)
            # if self.autoGainCheckBox.checkState() == QtCore.Qt.Checked:
            fft_frame /= np.abs(fft_frame).max()
                #print(np.abs(fft_frame).max())
            self.line_bottom.set_data(self.freq_vect, np.abs(fft_frame))

            # refreshes the plots
            self.main_figure.canvas.draw()


if __name__ == "__main__":
    app = QtGui.QApplication(sys.argv)
    window = LiveFFTWidget()
    sys.exit(app.exec_())
