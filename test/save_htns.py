import os, sys, getopt
sys.path.append('../')
import sptensor.hash as hash
import numpy as np
import time
import pickle

def main(argv):
    printTensor = False
    for arg in argv:
        if arg == "-print":
            printTensor = True

    file = sys.argv[1]
    outfile = sys.argv[2] #must end in .obj
    print('Saving to file: ', outfile)

    start_time = time.time()

    t = hash.read(file)

    print("--- %s seconds ---" % (time.time() - start_time))
    print("Max probe depth:", t.max_chain_depth)
    #print("cumulative probe time: ", t.probe_time)
    #print("number of collisions: ", t.num_collisions)

    object = t
    file = open(outfile, 'wb')
    pickle.dump(object, file)

    print("File has been saved.")

if __name__ == "__main__":
   main(sys.argv[1:])
