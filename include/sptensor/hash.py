
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

		#for i in range (buckets):
		#	table.append(sptensor_hash_item_t)

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
				return ptr.key

			# this is an empty position
			if ptr.flag == 0:
				ptr.morton = morton
				ptr.key = i
				#sptensor_index_cpy(t->modes, ptr->idx, idx)??
				return i

			# do linear probing
			t.num_collisions = t.num_collisions + 1
			i = (i+1) % t.nbuckets

		return -2

	#Function to insert an element in the hash table.
	def sptensor_hash_set(self, t, i, v):

		# get the hash item
		index = self.sptensor_hash_search(t, i)

		if index != -2:
			# either set or clear the item
			if v != 0:
				# mark as present
				t.hashtable[index].flag = 1

				# copy the value
				t.hashtable[index].value = v

				# Increase hashtable count
				t.hash_curr_size = t.hash_curr_size + 1
			else:
				# check if item is present in the table
				t.hashtable[index].flag = 1
				# remove it from the table
				print('removing value...')
				#self.sptensor_hash_remove(t, item)

				# Check if we need to rehash
				#if((t->hash_curr_size/t->nbuckets) > 0.8):
				#	sptensor_hash_rehash(t)
		return

	def sptensor_hash_get(self, index):
		print('to be implemented')

	def sptensor_hash_clear(self):
		print('to be implemented')

	def sptensor_hash_nnz(self):
		print('to be implemented')

	def sptensor_hash_read(self, file):
		print('to be implemented')

	def sptensor_hash_write(self, file):
		print('to be implemented')

	# Populate the mpz_t morton field with the morton encoding of the index.
	def sptensor_py_morton(self, nmodes, index):
		if len(nmodes) == 3:
			mortoncode = pm.interleave3(index[0], index[1], index[2])
			print(mortoncode)
			return mortoncode
