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

# Grab the JSON file contents
filePath = os.getcwd() + "/" + parser.parse_args().data
with open(filePath) as data_file:
    jsonFile = json.load(data_file)

# Declare data points and vocabulary (set of data points, no duplicates)
data = jsonFile["data"]
vocab = list(lst_set(data))
