from morton import morton

NBUCKETS = 128

class sptensor_hash_item_t:
	def __init__(self):
		self.morton = 0
		self.key = 0
		self.value = 0.0
		self.idx = []
		self.flag = 0

class sptensor_hash_t:
	def __init__(self, modes, nmodes):
		#sptensor fields
		self.modes = modes
		self.nmodes = nmodes

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
			table.append(sptensor_hash_item_t())

		return table

	def sptensor_hash_probe(self, t, i):

		i = i+1

		while 1:
			# set item to that index */
			item = t.hashtable[i]

			# this is an empty position */
			if item.flag == 0:
				item.key = i
				break

			# do linear probing
			t.num_collisions = t.num_collisions + 1
			i = (i+1) % t.nbuckets

		return item

	#Search the tensor for an index.
	def sptensor_hash_search(self, t, idx):

		#Compress idx using the morton encoding
		morton = self.sptensor_py_morton(t.nmodes, idx)

		#mod by number of buckets in hash and get the index
		i = morton % t.nbuckets

		# count the accesses
		t.num_accesses = t.num_accesses + 1

		# set item to that index
		item = t.hashtable[i]

		# If we do not have the right index, linearly probe
		if item.morton != morton:
			item = self.sptensor_hash_probe(t,i) #probe sets the key
		else:
			item.key = i

		item.morton = morton
		item.idx = idx

		return item

	#Function to insert an element in the hash table. Return the hash item if found, 0 if not found.
	def sptensor_hash_set(self, t, i, v):

		# get the hash item
		item = self.sptensor_hash_search(t, i)
		#print('item idx=',item.idx)
		#print('item key=',item.key)
		#print('item key=',item.key)

		# either set or clear the item
		if v != 0:
			# mark as present
			item.flag = 1

			# copy the value
			item.value = v

			# Increase hashtable count
			t.hash_curr_size = t.hash_curr_size + 1
		else:
			# check if item is present in the table
			#if (item.flag == 1):??
			# remove it from the table
			#print('removing value...')
			self.sptensor_hash_remove(t, item.idx)

		# Check if we need to rehash
		if((t.hash_curr_size/t.nbuckets) > 0.8):
			self.sptensor_hash_rehash(t)

		return

	def sptensor_hash_get(self, t, i):
		# get the hash item
		item = self.sptensor_hash_search(t, i);

		return item

	def sptensor_hash_clear(self, t):
		for i in range(t.nbuckets):
			t.hashtable[i].flag = 0
		return

	def sptensor_hash_rehash(self, t):
		# Double the number of buckets
		new_hash_size = t.nbuckets * 2
		new_hashtable = self.create_hashtable(new_hash_size)

		# save the old hash table
		old_hash_size = t.nbuckets;
		old_hashtable = t.hashtable;

		# install the new one
		t.nbuckets =  new_hash_size;
		t.hashtable = new_hashtable;

		# Rehash all existing items in t's hashtable to the new table
		for i in range(old_hash_size):
			item = old_hashtable[i]
			#If occupied, we need to copy it to the other table!
			if(item.flag == 1):
				self.sptensor_hash_set(t, item.idx, item.value)
		return

	def sptensor_hash_remove(self, t, idx):
		done = 0

		# get the index
		item = self.sptensor_hash_search(t, idx)
		i = item.key
		j = i+1

		# slide back as needed
		while(done == 0):
			# assume we are done
			done=1

			# mark as not present
			t.hashtable[i].flag = 0

			# go to the next probe slot
			j = (i+1)%j

			# check to see if we need to slide back
			if(t.hashtable[j].flag == 0):
				continue

			# check to see if this one should be pushed back
			if (t.hashtable[i].key == t.hashtable[j].key):
				#print('key[i] == key[j]')
				done = 0
				t.hashtable[i].flag = t.hashtable[j].flag
				t.hashtable[i].morton = t.hashtable[j].morton
				t.hashtable[i].value = t.hashtable[j].value
				t.hashtable[i].idx = t.hashtable[j].idx

			# go on for the next one */
			i=j

	def sptensor_hash_nnz(self):
		print('to be implemented')

	# Populate the mpz_t morton field with the morton encoding of the index.
	def sptensor_py_morton(self, nmodes, index):
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
		result = sptensor_hash_t(resultModes, len(resultModes))

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
				result.sptensor_hash_set(self, item.idx, item.value)
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
			return self.sptensor_hash_get(self, key)
	
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

		self.sptensor_hash_set(self, key, value)

def sptensor_hash_read(file):
	with open(file, 'r') as reader:
		# Get the modes and dimensions from the header
		first_line = reader.readline()
		idx = first_line.split()
		nmodes = int(idx.pop(0))

		idx = [int(i) for i in idx]

		# Create the tensor
		tns = sptensor_hash_t(idx, nmodes)

		for row in reader:
			row = row.split()
			# Get the value
			val = float(row.pop())
			# The rest of the line is the indexes
			idx = [int(i) for i in row]
			#print('idx: ',idx)
			#print('val: ',val)
			tns.sptensor_hash_set(tns, idx, val);

	reader.close()
	return tns

def sptensor_hash_write(file, tns):

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



