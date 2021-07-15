import os, sys, getopt
sys.path.append('../include/sptensor/')

import hash

def main(argv):

    modes = [3, 4, 5]
    idx = [ [1, 1, 1],
            [2, 3, 1],
            [2, 4, 4],
            [3, 2, 2]]

    v = [99.0, 44.0, 100.0, 1.0]


    tns = hash.sptensor_hash_t(modes, 3)
    print("created a tensor")

    '''#tns.sptensor_hash_set(tns, [4,4,4], 1.0);
    #print("set value")

    #item = tns.sptensor_hash_get(tns, [4,4,4]);
    #print("value = ", item.value)

    for i in range(tns.nbuckets):
        if tns.hashtable[i].flag == 1:
            print('idx:',tns.hashtable[i].idx)
            print('value:',tns.hashtable[i].value)

    #tns.sptensor_hash_set(tns, [2,1,1], 1.0);
    #print("set value")


    item = tns.sptensor_hash_get(tns, idx[0]);
    print("value = ", item.value)

    tns.sptensor_hash_remove(tns, idx[0]);
    print("removing...")

    new = tns.sptensor_hash_get(tns, idx[0]);
    print("value = ", new.value)
    '''

    file = sys.argv[1]
    print('file = ', file)

    t = hash.sptensor_hash_read(file)
    #hash.sptensor_hash_write(sys.stdout, t)

if __name__ == "__main__":
   main(sys.argv[1:])
