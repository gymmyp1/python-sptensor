import os, sys, getopt
sys.path.append('../')

import sptensor.hash as hash

import time

def main(argv):

    file = sys.argv[1]
    print('file: ', file)

    t = hash.read(file)
    hash.write(sys.stdout, t)

    for x in t.dense:
        print(x)

    #for x in t.nnz:
    #    print(x)

if __name__ == "__main__":
   main(sys.argv[1:])
