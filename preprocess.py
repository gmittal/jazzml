# Simple script to turn JSON data into a numpy array for use with RNN
# $ python preprocess.py /path/to/data.json datasetName

import argparse
import os
import numpy as np
import simplejson as json

# Used to filter duplicate objects out of data
def lst_set(lst):
    last = object()
    lst = sorted(lst, reverse=True)
    for item in lst:
        if item == last:
            continue
        yield item
        last = item

# Get command line arguments
parser = argparse.ArgumentParser(description='Data: JSON to Numpy Array Preprocesser.')
parser.add_argument('data', action="store", type=str)
parser.add_argument('dataset_name', action="store", type=str)
datasetName = parser.parse_args().dataset_name

# Grab the JSON file contents
filePath = os.getcwd() + "/" + parser.parse_args().data
with open(filePath) as data_file:
    jsonFile = json.load(data_file)

# Declare data points and assign index
data = jsonFile["data"]
vocab = list(lst_set(data))
data_ix = []
for index in range(0, len(data)):
    data_ix.append(vocab.index(data[index]))

os.makedirs(os.getcwd()+"/data/datasets/preprocessed/"+datasetName)
np.savetxt(os.getcwd()+"/data/datasets/preprocessed/"+datasetName+"/vocab.gz", vocab)
np.savetxt(os.getcwd()+"/data/datasets/preprocessed/"+datasetName+"/dataset.gz", data_ix)
