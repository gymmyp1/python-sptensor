import sys, getopt
sys.path.append('include/sptensor/')

import hash

def main():
    print('program start')
    modes = [3, 4, 5]
    idx = [ [1, 1, 1],
            [2, 3, 1],
            [2, 4, 4],
            [3, 2, 2]]

    v = [99.0, 44.0, 100.0, 1.0]

    tns = hash.sptensor_hash_t(modes, 3)
    #sptensor_hash_set(t, idx[i], mpfv);

    print("created a tensor")

if __name__ == "__main__":
   main()
