# Simulated tensor genor generator.
# Depending on specified tensor sparsity, generate number of nonzero
# entries.
# Does not produce any values, since only indexes are needed to
# test hashing method.

import os, sys, getopt
import random
import math
import datetime
import numpy as np
sys.path.append('../')

def main():
    dims = [10,7,5,6]
    sparsity = 0.9

    #tensor stuff
    modes = len(dims)
    print('number of modes = ', modes)

    total = 1
    for i in range(modes):
        total *= dims[i]

    print("total number of entries = ", total)

    #calculate number of nonzero entries
    nnz = math.ceil(total-(total*sparsity))

    with open(sys.argv[1], 'w') as file:
        #generate nnz's worth of triplets
        for i in range(nnz):
            for j in range(modes):
                file.write(str(random.randint(1, dims[j]))+" ")
            file.write('1\n')

    print("Sparse tensor generated.")

if __name__ == "__main__":
   main()
