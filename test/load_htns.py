import os, sys, getopt
sys.path.append('../')
import sptensor.hash as hash
import numpy as np
import pickle
import time

def main(argv):
    printTensor = False
    for arg in argv:
        if arg == "-print":
            printTensor = True

    file = sys.argv[-1]
    print('Loading file: ', file)

    f = open(file, 'rb')
    object = pickle.load(f)

    t= object

    print(t.table)
    print(t.modes)
    print(t.hash_curr_size)

if __name__ == "__main__":
   main(sys.argv[1:])
