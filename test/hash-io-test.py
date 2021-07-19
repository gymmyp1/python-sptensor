import os, sys, getopt
sys.path.append('../include/sptensor/')

import hash

def main(argv):

    tns = hash.sptensor_hash_t(modes, 3)

    file = sys.argv[1]
    print('file=', file)

    t = hash.sptensor_hash_read(file)
    hash.sptensor_hash_write(sys.stdout, t)

if __name__ == "__main__":
   main(sys.argv[1:])
