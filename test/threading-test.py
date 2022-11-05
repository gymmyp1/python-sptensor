#Looking at threading for mttkrp


import os, sys, getopt
sys.path.append('../')
import sptensor.hash as hash
import numpy as np
import time
import pickle

file = sys.argv[1]
print('Loading file: ', file)

f = open(file, 'rb')
object = pickle.load(f)
t = object
print("Import complete.")
