import os, sys, getopt
sys.path.append('../include/sptensor/')

import hash

def main(argv):

    file = sys.argv[1]
    #print('file: ', file)

    t = hash.read(file)
    #hash.write(sys.stdout, t)

if __name__ == "__main__":
   main(sys.argv[1:])
