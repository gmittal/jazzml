# Joey Alexander
Learning cool stuff about computers and jazz improvisation through [1 minute jazz lessons](https://www.youtube.com/playlist?list=PL7D9i_VsmDAQE1jJPsXmWYaEf5y6Wl8FQ).

Real-time jazz improvisation using fast Fourier transforms, digital signal processing (for real-time chord prediction) and machine learning techniques (for musical improvisation).


### Installation
The program requires quite a few dependencies, the most notable being:
  - Python 2.x+
  - fluidsynth
  - music21
  - mingus
  - tensorflow
  - PyAudio 0.2.9

To install all dependencies via ```pip```, simply run the following.
```none
$ pip install -r requirements.txt
```

### Running
The program attempts to improvise over chord changes that it detects in real-time via the microphone. Running the program without an external backing track doesn't lead to any particularly interesting results.

Running using the (boring and repetitive) defaults:

```none
$ python main.py
```

#### Training with Your Own Data
Create a JSON ```train.json``` file with the following format.

```javascript
{
  "data": [
    [2, 0.5],
    [3, 0.5],
    [4, 0.5],
    [5, 0.5],
    [3, 1],
    [1, 0.5],
    [2, 1]
  ]
}
```

Each element in the data array is a note, expressed with a scale degree and length in terms of beats — where 1 is a quarter note. If you have a better way for expressing these data files or for implementing more complex structure such as varying metres, please file a pull request.

Preprocess the raw ```train.json``` JSON file into a named dataset.

```none
$ python preprocess.py /path/to/train.json "my_dataset"
```

Now you can train the LSTM model on your dataset.

```none
$ python train.py /path/to/my_dataset
```

After you're done training for as long as you see fit, you can test your dataset was trained properly.

```none
$ python sample.py /path/to/my_dataset
```

You can then try it out to see how the machine improvises based on your dataset with the main program:

```none
$ python main.py
```

### License
The [MIT License](https://tldrlegal.com/license/mit-license#fulltext) (MIT)

Copyright (c) 2017 Gautam Mittal

Permission is hereby granted, free of charge, to any person obtaining a copy of this software and associated documentation files (the "Software"), to deal in the Software without restriction, including without limitation the rights to use, copy, modify, merge, publish, distribute, sublicense, and/or sell copies of the Software, and to permit persons to whom the Software is furnished to do so, subject to the following conditions:

The above copyright notice and this permission notice shall be included in all copies or substantial portions of the Software.

THE SOFTWARE IS PROVIDED "AS IS", WITHOUT WARRANTY OF ANY KIND, EXPRESS OR IMPLIED, INCLUDING BUT NOT LIMITED TO THE WARRANTIES OF MERCHANTABILITY, FITNESS FOR A PARTICULAR PURPOSE AND NONINFRINGEMENT. IN NO EVENT SHALL THE AUTHORS OR COPYRIGHT HOLDERS BE LIABLE FOR ANY CLAIM, DAMAGES OR OTHER LIABILITY, WHETHER IN AN ACTION OF CONTRACT, TORT OR OTHERWISE, ARISING FROM, OUT OF OR IN CONNECTION WITH THE SOFTWARE OR THE USE OR OTHER DEALINGS IN THE SOFTWARE.
