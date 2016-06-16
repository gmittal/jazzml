from __future__ import division
import math

class ChordDetector:
    def __init__(self):
        self.ChordQuality = ["Minor", "Major", "Suspended", "Dominant", "Diminshed5th", "Augmented5th"]
        self.bias = 1.06
        self.rootNote = 0
        self.quality = ""
        self.intervals = 0
        self.chromagram = [0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0]
        self.chordProfiles = [[0]*12]*108
        self.chord = [0]*108
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

        	# for j in range(0, 108):
            #     tmp = [];
            #     for t in range(0, 12):
        	# 		tmp.append(0)
            #     self.chordProfiles.append(tmp)

        	j = 0;

        	# major chords
        	for i in range(0, 12):
        		root = i % 12;
        		third = (i+4) % 12;
        		fifth = (i+7) % 12;

        		self.chordProfiles[j][root] = v1;
        		self.chordProfiles[j][third] = v2;
        		self.chordProfiles[j][fifth] = v3;

        		j+=1;

        	# minor chords
        	for i in range(0, 12):
        		root = i % 12;
        		third = (i+3) % 12;
        		fifth = (i+7) % 12;

        		self.chordProfiles[j][root] = v1;
        		self.chordProfiles[j][third] = v2;
        		self.chordProfiles[j][fifth] = v3;

        		j+=1;


        	# diminished chords
        	for i in range(0, 12):
        		root = i % 12;
        		third = (i+3) % 12;
        		fifth = (i+6) % 12;

        		self.chordProfiles[j][root] = v1;
        		self.chordProfiles[j][third] = v2;
        		self.chordProfiles[j][fifth] = v3;

        		j+=1;


        	# augmented chords
        	for i in range(0, 12):
        		root = i % 12;
        		third = (i+4) % 12;
        		fifth = (i+8) % 12;

        		self.chordProfiles[j][root] = v1;
        		self.chordProfiles[j][third] = v2;
        		self.chordProfiles[j][fifth] = v3;

        		j+=1;

        	# sus2 chords
        	for i in range(0, 12):
        		root = i % 12;
        		third = (i+2) % 12;
        		fifth = (i+7) % 12;

        		self.chordProfiles[j][root] = v1;
        		self.chordProfiles[j][third] = v2;
        		self.chordProfiles[j][fifth] = v3;

        		j+=1;

        	# sus4 chords
        	for i in range(0, 12):
        		root = i % 12;
        		third = (i+5) % 12;
        		fifth = (i+7) % 12;

        		self.chordProfiles[j][root] = v1;
        		self.chordProfiles[j][third] = v2;
        		self.chordProfiles[j][fifth] = v3;

        		j+=1;

        	# major 7th chords
        	for i in range(0, 12):
        		root = i % 12;
        		third = (i+4) % 12;
        		fifth = (i+7) % 12;
        		seventh = (i+11) % 12;

        		self.chordProfiles[j][root] = v1;
        		self.chordProfiles[j][third] = v2;
        		self.chordProfiles[j][fifth] = v3;
        		self.chordProfiles[j][seventh] = v3;

        		j+=1;

        	# minor 7th chords
        	for i in range(0, 12):
        		root = i % 12;
        		third = (i+3) % 12;
        		fifth = (i+7) % 12;
        		seventh = (i+10) % 12;

        		self.chordProfiles[j][root] = v1;
        		self.chordProfiles[j][third] = v2;
        		self.chordProfiles[j][fifth] = v3;
        		self.chordProfiles[j][seventh] = v3;

        		j+=1;


        	# dominant 7th chords
        	for i in range(0, 12):
        		root = i % 12;
        		third = (i+4) % 12;
        		fifth = (i+7) % 12;
        		seventh = (i+10) % 12;

        		self.chordProfiles[j][root] = v1;
        		self.chordProfiles[j][third] = v2;
        		self.chordProfiles[j][fifth] = v3;
        		self.chordProfiles[j][seventh] = v3;

        		j+=1;

            # print self.chordProfiles

    #=======================================================================
    def detectChord(self, chroma):
    	for i in range(0, 12):
    		self.chromagram[i] = chroma[i];

        # print chromagram
    	self.classifyChromagram(); print self.rootNote, self.quality, self.intervals;




    #=======================================================================
    def classifyChromagram(self):
    	i = int()
    	j = int()
    	fifth = int()
    	chordindex = int(); print self.chromagram


    	# remove some of the 5th note energy from chromagram
    	for i in range(0, 12):
    		fifth = (i+7) % 12;
    		self.chromagram[fifth] = self.chromagram[fifth] - (0.1*self.chromagram[i]);

    		if (self.chromagram[fifth] < 0):
    			self.chromagram[fifth] = 0;


    	# major chords
    	for j in range(0, 12):
    		self.chord[j] = self.calculateChordScore(self.chromagram,self.chordProfiles[j],self.bias,3);

    	# minor chords
    	for j in range(12, 24):
    		self.chord[j] = self.calculateChordScore(self.chromagram,self.chordProfiles[j],self.bias,3);

    	# diminished 5th chords
    	for j in range(24, 36):
    		self.chord[j] = self.calculateChordScore(self.chromagram,self.chordProfiles[j],self.bias,3);

    	# augmented 5th chords
    	for j in range(36, 48):
    		self.chord[j] = self.calculateChordScore(self.chromagram,self.chordProfiles[j],self.bias,3);

    	# sus2 chords
    	for j in range(48, 60):
    		self.chord[j] = self.calculateChordScore(self.chromagram,self.chordProfiles[j],1,3);

    	# sus4 chords
    	for j in range(60, 72):
    		self.chord[j] = self.calculateChordScore(self.chromagram,self.chordProfiles[j],1,3);

    	# major 7th chords
    	for j in range(72, 84):
    		self.chord[j] = self.calculateChordScore(self.chromagram,self.chordProfiles[j],1,4);

    	# minor 7th chords
    	for j in range(84, 96):
    		self.chord[j] = self.calculateChordScore(self.chromagram,self.chordProfiles[j],self.bias,4);

    	# dominant 7th chords
    	for j in range(96, 108):
    		self.chord[j] = self.calculateChordScore(self.chromagram,self.chordProfiles[j],self.bias,4);

    	chordindex = self.minimumIndex(self.chord,108);

    	# major
    	if (chordindex < 12):
    		self.rootNote = chordindex;
    		self.quality = 'Major';
    		self.intervals = 0;

    	# minor
    	if ((chordindex >= 12) and (chordindex < 24)):
    		self.rootNote = chordindex-12;
    		self.quality = 'Minor';
    		self.intervals = 0;

    	# diminished 5th
    	if ((chordindex >= 24) and (chordindex < 36)):
    		self.rootNote = chordindex-24;
    		self.quality = 'Dimished5th';
    		self.intervals = 0;

    	# augmented 5th
    	if ((chordindex >= 36) and (chordindex < 48)):
    		self.rootNote = chordindex-36;
    		self.quality = 'Augmented5th';
    		self.intervals = 0;

    	# sus2
    	if ((chordindex >= 48) and (chordindex < 60)):
    		self.rootNote = chordindex-48;
    		self.quality = 'Suspended';
    		self.intervals = 2;

    	# sus4
    	if ((chordindex >= 60) and (chordindex < 72)):
    		self.rootNote = chordindex-60;
    		self.quality = 'Suspended';
    		self.intervals = 4;

    	# major 7th
    	if ((chordindex >= 72) and (chordindex < 84)):
    		self.rootNote = chordindex-72;
    		self.quality = 'Major';
    		self.intervals = 7;

    	# minor 7th
    	if ((chordindex >= 84) and (chordindex < 96)):
    		self.rootNote = chordindex-84;
    		self.quality = 'Minor';
    		self.intervals = 7;

    	# dominant 7th
    	if ((chordindex >= 96) and (chordindex < 108)):
    		self.rootNote = chordindex-96;
    		self.quality = 'Dominant';
    		self.intervals = 7; print self.rootNote, self.quality, self.intervals

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
