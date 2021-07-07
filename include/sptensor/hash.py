
import pymorton as pm

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
		self.dim = nmodes

		#Hash specific fields
		self.nbuckets = NBUCKETS
		self.hashtable = self.create_hashtable(self.nbuckets,self.modes)
		self.hash_curr_size = 0
		self.num_collisions = 0
		self.num_accesses = 0
		self.probe_time = 0.0

	def create_hashtable(self, buckets, nmodes):
		table = [sptensor_hash_item_t()] * buckets * len(nmodes)

		return table

	#Search the tensor for an index.
	def sptensor_hash_search(self, t, idx):
		index = 0
		i = 0
		morton = 0

		#Compress idx using the morton encoding
		morton = self.sptensor_py_morton(t.modes, idx)

		#mod by number of buckets in hash and get the index
		index = morton % t.nbuckets
		i = index

		# count the accesses
		t.num_accesses = t.num_accesses + 1

		while 1:

			# set pointer to that index
			ptr = t.hashtable[i]

			# we have found the index in the table
			if ptr.morton == morton:
				return ptr

			# this is an empty position
			if ptr.flag == 0:
				return -1

			# do linear probing
			t.num_collisions = t.num_collisions + 1
			i = (i+1) % t.nbuckets

			if i == index:
				break

		return -1

	#Function to insert an element in the hash table. Return the hash item if found, 0 if not found.
	def sptensor_hash_set(self, t, i, v):

		# get the hash item
		item = self.sptensor_hash_search(t, i)

		if item != -1:
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
				print('removing value...')
				self.sptensor_hash_remove(t, item)

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
		new_hashtable = self.create_hashtable(new_hash_size,self.modes)

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
				sptensor_hash_set(t, item.idx, item.value)

		return

	def sptensor_hash_remove(self, t, idx):
		# get the index
		#i = ptr - t->hashtable;
		item = self.sptensor_hash_search(t, idx)
		item = sptensor_hash_item_t()

		'''done = 0

		# get the index
		#i = ptr - t->hashtable;
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
				print('key[i] == key[j]')
				done = 0
				t.hashtable[i].flag = t.hashtable[j].flag
				t.hashtable[i].morton = t.hashtable[j].morton
				t.hashtable[i].value = t.hashtable[j].value
				t.hashtable[i].idx = t.hashtable[j].idx

			# go on for the next one */
			i=j'''

	def sptensor_hash_nnz(self):
		print('to be implemented')


	def sptensor_hash_write(self, file):
		print('to be implemented')

	# Populate the mpz_t morton field with the morton encoding of the index.
	def sptensor_py_morton(self, nmodes, index):
		if len(nmodes) == 3:
			mortoncode = pm.interleave3(index[0], index[1], index[2])
			#print(mortoncode)
			return mortoncode

def sptensor_hash_read(file):
	with open(file, 'r') as reader:
		# Get the modes and dimensions from the header
		first_line = reader.readline()
		idx = first_line.split()
		nmodes = idx.pop(0)
		idx = [int(i) for i in idx]
		print('nmodes =',nmodes)
		for i in range(len(idx)):
			print(idx[i])

		# Create the tensor
		tns = sptensor_hash_t(idx, nmodes)

		for row in reader:
			row = row.split()
			# Get the value
			val = row.pop()
			# The rest of the line is the indexes
			idx = [int(i) for i in row]
			print('idx: ',idx)
			print('val: ',val)
			tns.sptensor_hash_set(tns, idx, val);

	reader.close()
