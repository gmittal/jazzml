from __future__ import division
import math

sampleFrequency = 4096
bufferSize = 8192
referenceFrequency = 130.81278265
numHarmonics = 2
numOctaves = 2
numBinsToSearch = 2
noteFrequencies = []
chromagram = [0.0]*12

for i in range(0, 12):
    noteFrequencies[i] = referenceFrequency*math.pow(12, i/12)

# take a frequency vector and then the audio values for each of those frequencies
def calculateChromagram(freq, m):
    divisorRatio = (samplingFrequency/4.0)/bufferSize
    for n in range(0, 12):
        chromaSum = 0.0
        for octave in range(1, numOctaves):
            noteSum = 0.0
            for harmonic in range(1, numHarmonics):
                int centerBin = math.round((noteFrequencies[n]*octave*harmonic)/divisorRatio)
                int minBin = centerBin - (numBinsToSearch*harmonic)
                int maxBin = centerBin + (numBinsToSearch*harmonic)

                maxVal = 0.0

                for k in range(minBin, maxBin):
                    if (m[k] > maxVal):
                        maxVal = m[k]

                noteSum += (maxVal / harmonic)

            chromaSum += noteSum

        chromagram[n] = chromaSum
    return chromagram
