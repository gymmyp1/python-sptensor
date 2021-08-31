import os, sys, getopt
sys.path.append('../')

import sptensor.hash as hash

import time

def main(argv):

    file = sys.argv[1]
    #print('file: ', file)

    start_time = time.time()

    t = hash.read(file)
    #hash.write(sys.stdout, t)

    print("--- %s seconds ---" % (time.time() - start_time))
    print("cumulative probe time: ", t.hashtable.probe_time)
    print("number of collisions: ", t.hashtable.num_collisions)

if __name__ == "__main__":
   main(sys.argv[1:])
