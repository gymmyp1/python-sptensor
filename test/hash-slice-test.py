import os, sys, getopt
sys.path.append('../include/sptensor/')

import hash

t = hash.hash_t((3,3,3))

for i in range(3):
    t[0,0,i] = i+1
    t[2,2,i] = i+2

print("Tensor")
hash.write(sys.stdout, t)

print("Index test")
for i in range(3):
    for j in range(3):
        for k in range(3):
            idx = (i,j,k)
            print(idx, '=>', t[idx])

print("Slice Test")
hash.write(sys.stdout, t[:,:,0])