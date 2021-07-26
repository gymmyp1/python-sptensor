# This program runs the hash function on a series of data. No probing takes place.
# This is inteneded to test the hash functions themseleves.
import os, sys, getopt
import math
sys.path.append('../')

from sptensor.morton import morton

# The hash ratio (before rehashing)
HASH_RATIO=0.8

# read the data in. It is assumed that the file contains information in the following format:
#   idx1 idx2 ... idxn value
# each index is stored as a tuple
indexes = []
with open(sys.argv[1], 'r') as file:
    for row in file:
        # read in the row and discard its value field
        row = row.split(' ')
        row.pop()

        # append the index
        indexes.append(tuple(int(i) for i in row))


# compute the size of the hash table
# We assume a starting size of 128, doubling each time a rehash would occur
reqSize = len(indexes) / HASH_RATIO
exp = int(math.ceil(math.log2(reqSize)))
nbuckets = max(128, 2**exp)


def hash(idx):
    """
    This is the hashing function. It returns the hash and the proposed key. For the
    given index.
    """
    m = morton(*idx)
    k = m % nbuckets

    return m, k

def jenkinsMortonHash(idx):
    m = morton(*idx)
    hash = m
    hash += hash << 3
    hash ^= hash >> 11
    hash += hash << 15
    k = hash % nbuckets
    return m, k


def jenkinsHash(idx):
    hash = 0
    for i in idx:
        hash += i
        hash += hash << 10
        hash ^= hash >> 6
    hash += hash << 3
    hash ^= hash >> 11
    hash += hash << 15

    return morton(*idx), hash%nbuckets



with open(sys.argv[2], 'w') as file:
    # print out the information about our table
    print("nbuckets", nbuckets, sep='\t', file=file)

    print('Morton', 'Key', sep='\t', file=file)
    # run the test on every value
    for idx in indexes:
        m, k = jenkinsMortonHash(idx)
        print(m, k, sep='\t', file=file)
