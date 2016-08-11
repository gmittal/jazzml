import argparse
import numpy as np
import simplejson as json

# Get command line arguments
parser = argparse.ArgumentParser(description='Data: JSON to Numpy Array Preprocesser.')
parser.add_argument('data', action="store", type=str)

filePath = parser.parse_args().data
