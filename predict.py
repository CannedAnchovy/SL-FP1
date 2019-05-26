import json
import numpy as np
import math
from argparse import ArgumentParser
import operator

parser = ArgumentParser()
parser.add_argument("-i", "--input_file", dest = "input_file", help = "Pass in a .json filename.")
parser.add_argument("-o", "--output_file", dest = "output_file", help = "Pass in a .json filename.")
args = parser.parse_args()
