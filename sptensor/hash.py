import time
import math
import sptensor.morton as mort
import numpy as np

NBUCKETS = 128


class hash_t:
	def __init__(self, modes=None):
		#Hash specific fields
		self.hash_curr_size = 0
		self.load_factor = 0.6

		#initialize the index hash
		self.hash_init(NBUCKETS)

		#iterators
		#self.dense = iter(self.dense_itr(self))
		#self.nnz = iter(self.nnz_itr(self))

		#sptensor fields
		self.modes = modes
		if modes:
			self.nmodes = len(modes)
		else:
			self.nmodes = 0

	'''Dense and non-zero iterator classes
	'''
	'''class dense_itr:
		def __init__(self, hash_type):
			self.table = hash_type.table
			self.nbuckets = hash_type.nbuckets

		def __iter__(self):
			self.bi = 0		#current bucket index
			self.li = 0		#current index in list
			return self

		def __next__(self):

			while self.bi < self.nbuckets:
				if self.table[self.bi] == None:
					self.bi += 1
					continue
					print('bi = ',self.bi)
					print('li = ',self.li)

				self.v = self.table[self.bi][self.li][1]
				self.li += 1

				#Are we at the end of the list?
				if self.li == len(self.table[self.bi]):
					self.li = 0
					self.bi += 1

				return self.v
			else:
				raise StopIteration

	class nnz_itr:
		def __init__(self, hash_type):
			self.hashtable = hash_type.hashtable
			self.nbuckets = hash_type.hashtable.nbuckets

		def __iter__(self):
			self.a = self.hashtable.value[0]
			self.i = 0
			return self

		def __next__(self):
			if self.i < self.nbuckets:
				#find the next non-zero value
				while self.hashtable.value[self.i] == 0.0:
					self.i += 1
					if self.i == self.nbuckets-1:
						raise StopIteration

				self.a = self.hashtable.value[self.i]
				self.i += 1
				return self.a
			else:
				raise StopIteration '''

	#Function to insert an element in the hash table. Return the hash item if found, 0 if not found.
	def set(self, i, v):
		# build the modes if we need
		if not self.modes:
			self.modes = [0] * len(i)
			self.nmodes = len(i)

		# update any mode maxes as needed
		for m in range(self.nmodes):
			if self.modes[m] < i[m]:
				self.modes[m] = i[m]

		# find the index
		morton = mort.encode(*i)
		k, i = self.search(morton)

		# insert accordingly
		if i == -1:
			if v != 0:
				if self.table[k] == None:
					self.table[k] = []
				self.table[k].append((morton, v))
				self.hash_curr_size = self.hash_curr_size + 1
				depth = len(self.table[k])
				if depth > self.max_chain_depth:
					self.max_chain_depth = depth
		else:
			if v !=0:
				self.table[k][i] = (morton, v)
			else:
				self.remove(k,i)


		# Check if we need to rehash
		if((self.hash_curr_size/self.nbuckets) > self.load_factor):
			self.rehash()


	def get(self, i):
		# get the hash item
		morton = mort.encode(*i)
		k, i = self.search(morton)

		# return the item if it is present
		if i != -1:
			return self.table[k][i][1]
		else:
			return 0.0


	def clear(self, ):
		for i in range(self.nbuckets):
			self.hash_init(self.nbuckets)
		return


	def rehash(self):
		old = self.table

		# Double the number of buckets
		self.hash_init(self.nbuckets * 2)

		# reinsert everything into the hash index
		for bucket in old:
			if not bucket:
				continue
			for item in bucket:
				k = self.hash(item[0])
				if self.table[k]==None:
					self.table[k] = []
				self.table[k].append(item)
				depth = len(self.table[k])
				if depth > self.max_chain_depth:
					self.max_chain_depth = depth



	def hash_init(self, nbuckets):
		self.nbuckets=nbuckets
		self.table=[None]*nbuckets
		self.bits = int(math.ceil(math.log2(self.nbuckets)))
		self.sx = int(math.ceil(self.bits/8)) - 1
		self.sy = 4*self.sx - 1
		if self.sy < 1:
			self.sy = 1
		self.sz = int(math.ceil(self.bits/2))
		self.mask = self.nbuckets-1
		self.num_collisions=0
		self.max_chain_depth=0
		self.probe_time=0
		
		'''print('sx =', self.sx)
		print('sy =', self.sy)
		print('sz =', self.sz)
		print('mask= ',self.mask)'''


	def hash(self, m):
		"""
		Hash the index and return the morton code and key.

		Parameters:
			m - The morton code to hash

		Returns:
			key
		"""
		hash = m
		hash += hash << self.sx
		hash ^= hash >> self.sy
		hash += hash << self.sz
		k = hash % self.nbuckets
		
		#print('hash << sx= ', hash)
		#print('hash << sy= ', hash)
		#print('hash << sz= ', hash)
		#print("k=",k);
		
		return k


	def search(self, m):
		"""
		Search for a morton coded entry in the index hash.
		Parameters:
			m - The morton entry
		Returns:
			If m is found, it returns the (k, i) tuple where k is
			  the bucket and i is the index in the chain
			if m is not found, it returns (k, -1).
		"""
		k = self.hash(m)
		if self.table[k] != None:
			for i, item in enumerate(self.table[k]):
				if item[0] == m:
					return (k, i)
		return (k, -1)



	def remove(self, k, i):
		self.table[k].pop(i)


	def get_slice(self, key):
		# make it a list!
		key = list(key)

		# convert all keys into ranges and extract modes
		resultModes = []
		for i in range(len(key)):
			if type(key[i]) == slice:
				key[i] = range(*key[i].indices(self.modes[i]))
			else:
				key[i] = range(key[i], key[i]+1)
			resultModes.append(len(key[i]))

		# create the result tensor
		result = hash_t(resultModes)

		# copy the relevant non-zeroes
		for index in range(self.nbuckets):
			#skip the not-present
			if self.hashtable.flag[index] != 1:
				continue

			# copy the things in our range
			copy = True
			idx = mort.decode(self.hashtable.morton[index], self.nmodes)
			for i in range(len(idx)):
				if idx[i] not in key[i]:
					copy = False
					break
			if copy:
				result.set(idx, self.hashtable.value[index])
		return result


	def __getitem__(self, key):
		# make the key iteratble (if needed)
		if not hasattr(key, '__iter__'):
			key = (key,)

		# validate the index
		if len(key) != self.nmodes:
			raise IndexError("Mode Mismatch")
		simpleIndex = True
		for i in key:
			if type(i)==slice:
				simpleIndex = False
			elif type(i) != int:
				raise IndexError("Mode index must be either a slice or an integer.")

		# handle simple index
		if simpleIndex:
			return self.get(key)

		# do the extra work
		return self.get_slice(key)


	def __setitem__(self, key, value):
		# make the key iteratble (if needed)
		if not hasattr(key, '__iter__'):
			key = (key,)

		# validate the index
		if len(key) != self.nmodes:
			raise IndexError("Mode Mismatch")
		for i in key:
			if type(i) != int:
				raise IndexError("Mode index must be an integer.")

		self.set(key, value)


	def mttkrp(self, u, n):
		'''
		Carry out mttkrp between the tensor and an array of matrices,
		unfolding the tensor along mode n.

		Parameters:
			u - A list of numpy matrices, these correspond to the modes
				in the tensor, other than n. If i is the dimension in
				mode x, then u[x] must be an i x f matrix.
			n - The mode along which the tensor is unfolded for the
				product.
		Returns:
			A numpy matrix with dimensions i_n x f
		'''

		# number of columns
		fmax = u[0].shape[1]

		# create the result array
		m = np.zeros((self.modes[n], fmax))

		# go through each column
		for f in range(fmax):
			# accumulation arrays
			z=0
			t=[]
			tind=[]

			# go through every non-zero
			for bucket in self.table:
				if bucket == None:
					continue
				for entry in bucket:
					idx = mort.decode(entry[0], self.nmodes)
					t.append(entry[1])
					tind.append(idx[n])
					z = len(t) -1

					# multiply by the factor matrix entries
					i=0
					for b in u:
						# skip the unfolded mode
						if i==n:
							i += 1
							continue

						# multiply the factor and advance to the next
						t[z] *= b[idx[i], f]
						i += 1
			# end for
			# accumulate m(:,f)
			for z in range(len(t)):
				m[tind[z],f] = m[tind[z], f] + t[z]
			# end for
		# end for
		return m



def read(file):
	with open(file, 'r') as reader:
		# Create the tensor
		tns = hash_t()
		
		for row in reader:
			row = row.split()
			# Get the value
			val = float(row.pop())
			# The rest of the line is the indexes
			idx = [int(i) for i in row]

			tns.set(idx, val)

	reader.close()
	return tns

def write(file, tns):
	for bucket in tns.table:
		if bucket == None:
			continue
		for item in bucket:
			print(*mort.decode(item[0], tns.nmodes), item[1])
