# This program runs the hash function on a series of data. No probing takes place.
# This is inteneded to test the hash functions themseleves.
import os, sys, getopt
import math
import binascii
sys.path.append('../')

from sptensor.morton import encode

# The hash ratio (before rehashing)
HASH_RATIO=0.7

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
bits = max(exp, 7)
x = int(math.ceil(bits/8)) - 1
y = 4*x - 1
z = int(math.ceil(bits/2))

def hash(idx):
    """
    This is the hashing function. It returns the hash and the proposed key. For the
    given index.
    """
    m = encode(*idx)
    k = m % nbuckets

    return m, k

def crc(idx):
    # Converting integer list to string list
    s = [str(i) for i in idx]
    # Join list items using join()
    m = ''.join(s)
    text_bytes = bytes(m,'utf-8')
    m = binascii.crc32(text_bytes)
    k = int(m) % nbuckets
    return m, k

def jenkinsMortonHash(idx):
    #m = encode(*idx)
    # Converting integer list to string list
    s = [str(i) for i in idx]
    # Join list items using join()
    m = int("".join(s))
    hash = m
    hash += hash << x
    hash ^= hash >> y
    hash += hash << z
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

    return encode(*idx), hash%nbuckets



with open(sys.argv[2], 'w') as file:
    # print out the information about our table
    print("nbuckets", nbuckets, sep='\t', file=file)

    print('Morton', 'Key', sep='\t', file=file)
    # run the test on every value
    for idx in indexes:
        m, k = crc(idx)
        print(m, k, sep='\t', file=file)
