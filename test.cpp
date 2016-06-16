#include <iostream>
#include "chords/src/ChordDetector.h"

int main() {
  ChordDetector chordDetector;
  double chroma[12] = {1,0,0,0,1,0,0,1,0,0,0,0};
  std::string roots[12] = {"C", "Db", "D", "Eb", "E", "F", "Gb", "G", "Ab", "A", "Bb", "B"};
  std::string quality[6]= {"Min","Maj","Sus","","-","+"};
  chordDetector.detectChord(chroma);
  std::cout << "Value of str is : " << roots[chordDetector.rootNote] << "" << quality[chordDetector.quality] << "" << chordDetector.intervals << std::endl;
}
