import os, sys, getopt
sys.path.append('../')

import sptensor.hash as hash

import time

def main(argv):
    print('hello')
    file = sys.argv[1]
    print('file: ', file)

    t = hash.read(file)
    hash.write(sys.stdout, t)

    myiter = iter(t)

    for x in myiter:
        print(x)

if __name__ == "__main__":
   main(sys.argv[1:])
