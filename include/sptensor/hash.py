from tqdm import tqdm
import time

from morton import morton

NBUCKETS = 128

class hash_item_t:
	def __init__(self):
		self.morton = None
		self.key = 0
		self.value = 0.0
		self.idx = []
		self.flag = 0

class hash_t:
	def __init__(self, modes):
		#sptensor fields
		self.modes = modes
		self.nmodes = len(modes)

		#Hash specific fields
		self.nbuckets = NBUCKETS
		self.hashtable = self.create_hashtable(self.nbuckets)
		self.hash_curr_size = 0
		self.num_collisions = 0
		self.num_accesses = 0
		self.probe_time = 0.0

	def create_hashtable(self, nbuckets):
		table = []

		for i in range(nbuckets):
			table.append(hash_item_t())

		return table

	#Search the tensor for an index.
	def search(self, idx):

		#Compress idx using the morton encoding
		morton = self.morton(idx)

		#mod by number of buckets in hash and get the index
		i = morton % self.nbuckets

		# count the accesses
		self.num_accesses = self.num_accesses + 1

		while(1):
			# set item to that index
			item = self.hashtable[i]

			# If we do not have the right index, linearly probe
			if item.morton == morton:
				#print('item.morton != morton')
				#item = self.sptensor_hash_probe(t,i) #probe sets the key
				break

			if item.flag == 0:
				item.key
				item.morton = morton
				item.idx = idx
				break

			# do linear probing
			self.num_collisions = self.num_collisions + 1
			i = (i+1) % self.nbuckets

		return item

	#Function to insert an element in the hash table. Return the hash item if found, 0 if not found.
	def set(self, i, v):

		# get the hash item
		item = self.search(i)

		# either set or clear the item
		if v != 0:
			# mark as present
			item.flag = 1

			# copy the value
			item.value = v

			# Increase hashtable count
			self.hash_curr_size = self.hash_curr_size + 1
		else:
			# check if item is present in the table
			#if (item.flag == 1):??
			# remove it from the table
			#print('removing value...')
			self.remove(item.idx)

		# Check if we need to rehash
		if((self.hash_curr_size/self.nbuckets) > 0.8):
			self.rehash()

		return

	def get(self, i):
		# get the hash item
		item = self.search(i)
		#print('item.idx=', item.idx)
		#print('item.value= ',item.value)
		#print('item.key= ',item.key)
		return item.value

	def clear(self, ):
		for i in range(self.nbuckets):
			self.hashtable[i].flag = 0
		return

	def rehash(self):
		#print('rehashing...')

		# Double the number of buckets
		new_hash_size = self.nbuckets * 2
		new_hashtable = self.create_hashtable(new_hash_size)

		# save the old hash table
		old_hash_size = self.nbuckets
		old_hashtable = self.hashtable

		# install the new one
		self.nbuckets =  new_hash_size
		self.hashtable = new_hashtable

		# Rehash all existing items in t's hashtable to the new table
		for i in range(old_hash_size):
			item = old_hashtable[i]
			#If occupied, we need to copy it to the other table!
			if(item.flag == 1):
				self.set(item.idx, item.value)
		return

	def remove(self, idx):
		done = 0

		# get the index
		item = self.search(idx)
		i = item.key
		j = i+1

		# slide back as needed
		while(done == 0):
			# assume we are done
			done=1

			# mark as not present
			self.hashtable[i].flag = 0

			# go to the next probe slot
			j = (i+1)%j

			# check to see if we need to slide back
			if(self.hashtable[j].flag == 0):
				continue

			# check to see if this one should be pushed back
			if (self.hashtable[i].key == self.hashtable[j].key):
				#print('key[i] == key[j]')
				done = 0
				self.hashtable[i].flag = self.hashtable[j].flag
				self.hashtable[i].morton = self.hashtable[j].morton
				self.hashtable[i].value = self.hashtable[j].value
				self.hashtable[i].idx = self.hashtable[j].idx

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
		for item in self.hashtable:
			#skip the not-present
			if item.flag != 1:
				continue

			# copy the things in our range
			copy = True
			for i in range(len(item.idx)):
				if item.idx[i] not in key[i]:
					copy = False
					break
			if copy:
				result.set(item.idx, item.value)
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
	for i in tqdm(range(100),desc='Reading file'):
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
				#print('idx: ',idx)
				#print('val: ',val)
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
		item = tns.hashtable[i]
		if item.flag == 1:
			# print the indexes
			for j in range(tns.nmodes):
				print(item.idx[j], end=' ')

			#print the value
			print(item.value)
