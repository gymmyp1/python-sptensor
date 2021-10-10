import os, sys, getopt
sys.path.append('../')
import sptensor.hash as hash
import numpy as np

# the tensor
t = hash.hash_t((2,3,2))
t[0,0,0]=1
t[0,1,0]=2
t[0,2,0]=3
t[1,0,0]=4
t[1,1,0]=5
t[1,2,0]=6
t[0,0,1]=7
t[0,1,1]=8
t[0,2,1]=9
t[1,0,1]=10
t[1,1,1]=11
t[1,2,1]=12

# the test factor matrices
a = np.matrix('1 3 5; 2 4 6')
b = np.matrix('1 4 7; 2 5 8; 3 6 9')
c = np.matrix('1 2 3; 4 5 6')
u = (a, b, c)

# try out each multiplication
print(t.mttkrp(u, 0))
print(t.mttkrp(u, 1))
print(t.mttkrp(u, 2))
