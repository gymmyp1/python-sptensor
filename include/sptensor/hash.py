import time

from morton import morton

NBUCKETS = 128

class HashTable:
	def __init__(self, nbuckets):
		self.nbuckets = nbuckets
		self.morton = [None] * nbuckets
		self.key = [0] * nbuckets
		self.value = [0.0] * nbuckets
		self.idx = [None] * nbuckets
		self.flag = [0] * nbuckets

class hash_t:
	def __init__(self, modes):
		#sptensor fields
		self.modes = modes
		self.nmodes = len(modes)

		#Hash specific fields
		self.nbuckets = NBUCKETS
		self.hashtable = HashTable(self.nbuckets)
		self.hash_curr_size = 0
		self.num_collisions = 0
		self.num_accesses = 0
		self.probe_time = 0.0


	#Search the tensor for an index.
	def search(self, idx):

		#Compress idx using the morton encoding
		morton = self.morton(idx)

		#mod by number of buckets in hash and get the index
		i = morton % self.nbuckets

		# count the accesses
		self.num_accesses = self.num_accesses + 1

		while(1):
			# If we do not have the right index, linearly probe
			if self.hashtable.morton[i] == morton:
				break

			if self.hashtable.flag[i] == 0:
				self.hashtable.key[i]
				self.hashtable.morton[i] = morton
				self.hashtable.idx[i] = idx
				break

			# do linear probing
			self.num_collisions = self.num_collisions + 1
			i = (i+1) % self.nbuckets

		return i

	#Function to insert an element in the hash table. Return the hash item if found, 0 if not found.
	def set(self, i, v):

		# get the hash item
		index = self.search(i)

		# either set or clear the item
		if v != 0:
			# mark as present
			self.hashtable.flag[index] = 1

			# copy the value
			self.hashtable.value[index] = v

			# Increase hashtable count
			self.hash_curr_size = self.hash_curr_size + 1
		else:
			# check if item is present in the table
			if self.hashtable.flag[index] == 1:
				# remove it from the table
				self.remove(i)

		# Check if we need to rehash
		if((self.hash_curr_size/self.nbuckets) > 0.8):
			self.rehash()

		return

	def get(self, i):
		# get the hash item
		i = self.search(i)

		return self.hashtable.value[i]

	def clear(self, ):
		for i in range(self.nbuckets):
			self.hashtable.flag[i] = 0
		return


	def rehash(self):

		# Double the number of buckets
		new_hash_size = self.nbuckets * 2
		new_hashtable = HashTable(new_hash_size)

		# save the old hash table
		old_hash_size = self.nbuckets
		old_hashtable = self.hashtable

		# install the new one
		self.nbuckets =  new_hash_size
		self.hashtable = new_hashtable

		# Rehash all existing items in t's hashtable to the new table
		for i in range(old_hash_size):
			#If occupied, we need to copy it to the other table!
			if(self.hashtable.flag[i] == 1):
				self.set(self.hashtable.idx[i], self.hashtable.value[i])


	def remove(self, idx):
		done = 0

		# get the index
		index = self.search(idx)
		i = self.hashtable.key[index]
		j = i+1

		# slide back as needed
		while(done == 0):
			# assume we are done
			done=1

			# mark as not present
			self.hashtable.flag[i] = 0

			# go to the next probe slot
			j = (i+1)%j

			# check to see if we need to slide back
			if(self.hashtable.flag[j] == 0):
				continue

			# check to see if this one should be pushed back
			if (self.hashtable.key[j] == self.hashtable.key[j]):
				#print('key[i] == key[j]')
				done = 0
				self.hashtable.flag[i] = self.hashtable.flag[j]
				self.hashtable.morton[i] = self.hashtable.morton[j]
				self.hashtable.value[i] = self.hashtable.value[j]
				self.hashtable.idx[i] = self.hashtable.idx[j]

			# go on for the next one */
			i=j

	def nnz(self):
		print('to be implemented')

	# Populate the mpz_t morton field with the morton encoding of the index.
	def morton(self, index):
		return morton(*index)


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
		for index in range(self.hashtable.nbuckets):
			#skip the not-present
			if self.hashtable.flag[index] != 1:
				continue

			# copy the things in our range
			copy = True
			for i in range(len(self.hashtable.idx[index])):
				if self.hashtable.idx[index][i] not in key[i]:
					copy = False
					break
			if copy:
				result.set(self.hashtable.idx[index], self.hashtable.value[index])
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

def read(file):
	with open(file, 'r') as reader:
		# Get the modes and dimensions from the header
		first_line = reader.readline()
		idx = first_line.split()
		nmodes = int(idx.pop(0))

		idx = [int(i) for i in idx]

		# Create the tensor
		tns = hash_t(idx)

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

	# print the preamble
	print(tns.nmodes, end=' ')
	for i in range(tns.nmodes):
		print(tns.modes[i], end=' ')

	print('\n',end='')

	for i in range(tns.nbuckets):
		if tns.hashtable.flag[i] == 1:
			# print the indexes
			for j in range(tns.nmodes):
				print(tns.hashtable.idx[i][j], end=' ')

			#print the value
			print(tns.hashtable.value[i])
