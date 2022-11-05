import os, sys, getopt
sys.path.append('../')
import sptensor.hash as hash
import numpy as np
import time
import pickle

'''
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
'''


file = sys.argv[1]
print('Loading file: ', file)

f = open(file, 'rb')
object = pickle.load(f)
t = object
print("Import complete.")

start_time = time.time()

# create factor matrices
#This correcponds to the number of components in the decomposition
colsz = 50
u = []
for i in range(t.nmodes):
    u.append(np.random.rand(t.modes[i],colsz))

# try out each multiplication
print(t.mttkrp(u, 0))
print(t.mttkrp(u, 1))
print(t.mttkrp(u, 2))

print("--- %s seconds ---" % (time.time() - start_time))
