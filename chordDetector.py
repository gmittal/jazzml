from __future__ import division
import math

class ChordDetector:
    ChordQuality = ["min", "maj", "sus", "", "-", "+"]
    bias = 1.06
    rootNote = 0
    quality = ""
    intervals = 0
    chromagram = [0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0]
    chordProfiles = []
    chord = [0]*108

    for j in range(0, 108):
        tmp = [];
        for t in range(0, 12):
            tmp.append(0)
        chordProfiles.append(tmp)

    def __init__(self):
        self.makechordProfiles()

    def makechordProfiles(self):
        	i = int()
        	t = int()
        	j = 0
        	root = int()
        	third = int()
        	fifth = int()
        	seventh = int()

        	v1 = 1
        	v2 = 1;
        	v3 = 1;



        	j = 0;

        	# major chords
        	for i in range(0, 12):
        		root = i % 12;
        		third = (i+4) % 12;
        		fifth = (i+7) % 12;

        		ChordDetector.chordProfiles[j][root] = v1;
        		ChordDetector.chordProfiles[j][third] = v2;
        		ChordDetector.chordProfiles[j][fifth] = v3;

        		j+=1;

        	# minor chords
        	for i in range(0, 12):
        		root = i % 12;
        		third = (i+3) % 12;
        		fifth = (i+7) % 12;

        		ChordDetector.chordProfiles[j][root] = v1;
        		ChordDetector.chordProfiles[j][third] = v2;
        		ChordDetector.chordProfiles[j][fifth] = v3;

        		j+=1;


        	# diminished chords
        	for i in range(0, 12):
        		root = i % 12;
        		third = (i+3) % 12;
        		fifth = (i+6) % 12;

        		ChordDetector.chordProfiles[j][root] = v1;
        		ChordDetector.chordProfiles[j][third] = v2;
        		ChordDetector.chordProfiles[j][fifth] = v3;

        		j+=1;


        	# augmented chords
        	for i in range(0, 12):
        		root = i % 12;
        		third = (i+4) % 12;
        		fifth = (i+8) % 12;

        		ChordDetector.chordProfiles[j][root] = v1;
        		ChordDetector.chordProfiles[j][third] = v2;
        		ChordDetector.chordProfiles[j][fifth] = v3;

        		j+=1;

        	# sus2 chords
        	for i in range(0, 12):
        		root = i % 12;
        		third = (i+2) % 12;
        		fifth = (i+7) % 12;

        		ChordDetector.chordProfiles[j][root] = v1;
        		ChordDetector.chordProfiles[j][third] = v2;
        		ChordDetector.chordProfiles[j][fifth] = v3;

        		j+=1;

        	# sus4 chords
        	for i in range(0, 12):
        		root = i % 12;
        		third = (i+5) % 12;
        		fifth = (i+7) % 12;

        		ChordDetector.chordProfiles[j][root] = v1;
        		ChordDetector.chordProfiles[j][third] = v2;
        		ChordDetector.chordProfiles[j][fifth] = v3;

        		j+=1;

        	# major 7th chords
        	for i in range(0, 12):
        		root = i % 12;
        		third = (i+4) % 12;
        		fifth = (i+7) % 12;
        		seventh = (i+11) % 12;

        		ChordDetector.chordProfiles[j][root] = v1;
        		ChordDetector.chordProfiles[j][third] = v2;
        		ChordDetector.chordProfiles[j][fifth] = v3;
        		ChordDetector.chordProfiles[j][seventh] = v3;

        		j+=1;

        	# minor 7th chords
        	for i in range(0, 12):
        		root = i % 12;
        		third = (i+3) % 12;
        		fifth = (i+7) % 12;
        		seventh = (i+10) % 12;

        		ChordDetector.chordProfiles[j][root] = v1;
        		ChordDetector.chordProfiles[j][third] = v2;
        		ChordDetector.chordProfiles[j][fifth] = v3;
        		ChordDetector.chordProfiles[j][seventh] = v3;

        		j+=1;


        	# dominant 7th chords
        	for i in range(0, 12):
        		root = i % 12;
        		third = (i+4) % 12;
        		fifth = (i+7) % 12;
        		seventh = (i+10) % 12;

        		ChordDetector.chordProfiles[j][root] = v1;
        		ChordDetector.chordProfiles[j][third] = v2;
        		ChordDetector.chordProfiles[j][fifth] = v3;
        		ChordDetector.chordProfiles[j][seventh] = v3;

        		j+=1;

            # print ChordDetector.chordProfiles

    #=======================================================================
    def detectChord(self, chroma):
    	for i in range(0, 12):
    		ChordDetector.chromagram[i] = chroma[i];

        # print chromagram
    	self.classifyChromagram();




    #=======================================================================
    def classifyChromagram(self):
    	i = int()
    	j = int()
    	fifth = int()
    	chordindex = int(); #print ChordDetector.chromagram


    	# remove some of the 5th note energy from ChordDetector.chromagram
    	for i in range(0, 12):
    		fifth = (i+7) % 12;
    		ChordDetector.chromagram[fifth] = ChordDetector.chromagram[fifth] - (0.1*ChordDetector.chromagram[i]);

    		if (ChordDetector.chromagram[fifth] < 0):
    			ChordDetector.chromagram[fifth] = 0;


    	# major chords
    	for j in range(0, 12):
    		ChordDetector.chord[j] = self.calculateChordScore(ChordDetector.chromagram,ChordDetector.chordProfiles[j],ChordDetector.bias,3);

    	# minor chords
    	for j in range(12, 24):
    		ChordDetector.chord[j] = self.calculateChordScore(ChordDetector.chromagram,ChordDetector.chordProfiles[j],ChordDetector.bias,3);

    	# diminished 5th chords
    	for j in range(24, 36):
    		ChordDetector.chord[j] = self.calculateChordScore(ChordDetector.chromagram,ChordDetector.chordProfiles[j],ChordDetector.bias,3);

    	# augmented 5th chords
    	for j in range(36, 48):
    		ChordDetector.chord[j] = self.calculateChordScore(ChordDetector.chromagram,ChordDetector.chordProfiles[j],ChordDetector.bias,3);

    	# sus2 chords
    	for j in range(48, 60):
    		ChordDetector.chord[j] = self.calculateChordScore(ChordDetector.chromagram,ChordDetector.chordProfiles[j],1,3);

    	# sus4 chords
    	for j in range(60, 72):
    		ChordDetector.chord[j] = self.calculateChordScore(ChordDetector.chromagram,ChordDetector.chordProfiles[j],1,3);

    	# major 7th chords
    	for j in range(72, 84):
    		ChordDetector.chord[j] = self.calculateChordScore(ChordDetector.chromagram,ChordDetector.chordProfiles[j],1,4);

    	# minor 7th chords
    	for j in range(84, 96):
    		ChordDetector.chord[j] = self.calculateChordScore(ChordDetector.chromagram,ChordDetector.chordProfiles[j],ChordDetector.bias,4);

    	# dominant 7th chords
    	for j in range(96, 108):
    		ChordDetector.chord[j] = self.calculateChordScore(ChordDetector.chromagram,ChordDetector.chordProfiles[j],ChordDetector.bias,4);

    	chordindex = self.minimumIndex(ChordDetector.chord,108);

    	# major
    	if (chordindex < 12):
    		ChordDetector.rootNote = chordindex;
    		ChordDetector.quality = 'maj';
    		ChordDetector.intervals = 0;

    	# minor
    	if ((chordindex >= 12) and (chordindex < 24)):
    		ChordDetector.rootNote = chordindex-12;
    		ChordDetector.quality = 'min';
    		ChordDetector.intervals = 0;

    	# diminished 5th
    	if ((chordindex >= 24) and (chordindex < 36)):
    		ChordDetector.rootNote = chordindex-24;
    		ChordDetector.quality = '-';
    		ChordDetector.intervals = 0;

    	# augmented 5th
    	if ((chordindex >= 36) and (chordindex < 48)):
    		ChordDetector.rootNote = chordindex-36;
    		ChordDetector.quality = '+';
    		ChordDetector.intervals = 0;

    	# sus2
    	if ((chordindex >= 48) and (chordindex < 60)):
    		ChordDetector.rootNote = chordindex-48;
    		ChordDetector.quality = 'sus';
    		ChordDetector.intervals = 2;

    	# sus4
    	if ((chordindex >= 60) and (chordindex < 72)):
    		ChordDetector.rootNote = chordindex-60;
    		ChordDetector.quality = 'sus';
    		ChordDetector.intervals = 4;

    	# major 7th
    	if ((chordindex >= 72) and (chordindex < 84)):
    		ChordDetector.rootNote = chordindex-72;
    		ChordDetector.quality = 'maj';
    		ChordDetector.intervals = 7;

    	# minor 7th
    	if ((chordindex >= 84) and (chordindex < 96)):
    		ChordDetector.rootNote = chordindex-84;
    		ChordDetector.quality = 'min';
    		ChordDetector.intervals = 7;

    	# dominant 7th
    	if ((chordindex >= 96) and (chordindex < 108)):
    		ChordDetector.rootNote = chordindex-96;
    		ChordDetector.quality = '';
    		ChordDetector.intervals = 7;

    #=======================================================================
    def calculateChordScore(self, chroma,chordProfile,biasToUse,N):
    	sum = 0;
    	delta = 0;

    	for i in range(0, 12):
    		sum += (((1-chordProfile[i])*(chroma[i]*chroma[i])));

    	delta = (math.sqrt(sum) / ((12 - N)*biasToUse));

    	return delta

    #=======================================================================
    def minimumIndex(self, array,arrayLength):
    	minValue = 100000;
    	minIndex = 0;

    	for i in range(0, arrayLength):
    		if (array[i] < minValue):
    			minValue = array[i];
    			minIndex = i;

    	return minIndex;
