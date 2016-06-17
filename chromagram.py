from __future__ import division
import math

samplingFrequency = 2000
bufferSize = 1024
referenceFrequency = 130.81278265 # C
numHarmonics = 2
numOctaves = 4
numBinsToSearch = 2
noteFrequencies = []
chromagram = [0.0000000000000000000]*12

for i in range(0, 12):
    noteFrequencies.append(referenceFrequency*math.pow(2, i/12))

print noteFrequencies
# take a frequency vector and then the audio values for each of those frequencies
def calculateChromagram(freq, m):
    divisorRatio = (samplingFrequency/4.0)/bufferSize
    for n in range(0, 12):
        chromaSum = 0
        for octave in range(1, numOctaves):
            noteSum = 0
            for harmonic in range(1, numHarmonics):
                # print "HARMONICS"
                # print n
                centerBin = round((noteFrequencies[n]*octave*harmonic)/divisorRatio)
                minBin = centerBin - (numBinsToSearch*harmonic)
                maxBin = centerBin + (numBinsToSearch*harmonic)

                minIndex = min(range(len(freq)), key=lambda i: abs(freq[i]-minBin))
                maxIndex = min(range(len(freq)), key=lambda i: abs(freq[i]-maxBin))

                # print minBin, maxBin
                # print freq[minIndex], freq[maxIndex]
                # print m[minIndex], m[maxIndex]

                maxVal = 0

                for k in range(int(minIndex), int(maxIndex)):
                    if (m[k] > maxVal):
                        maxVal = m[k]
                        # print n
                        # print m[k]

                noteSum += (maxVal / harmonic)
                # print noteSum

            chromaSum += noteSum
            # print chromaSum

        # print n, chromaSum
        chromagram[n] = chromaSum
    return chromagram
