import os, sys, getopt
sys.path.append('../include/sptensor/')

import hash

def main():

    modes = [3, 4, 5]
    idx = [ [1, 1, 1],
            [2, 3, 1],
            [2, 4, 4],
            [3, 2, 2]]

    v = [99.0, 44.0, 100.0, 1.0]

    tns = hash.hash_t(modes)

    tns.set([4,4,4], 5.0);
    print("set value")

    value = tns.get([4,4,4]);
    print("value = ", value)

    tns.remove(idx[0]);
    print("removing...")

    new = tns.get(idx[0]);
    print("value = ", new)

    '''for i in range(tns.nbuckets):
        if tns.hashtable[i].flag == 1:
            print('idx:',tns.hashtable[i].idx)
            print('value:',tns.hashtable[i].value)'''


if __name__ == "__main__":
   main()
