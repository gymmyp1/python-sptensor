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
    print("created a tensor")
    tns.sptensor_hash_set(tns, idx[0], 99.0);

    print("set value")

if __name__ == "__main__":
   main()
