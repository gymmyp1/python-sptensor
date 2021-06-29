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
        table = []

        for i in range (buckets):
            table.append(sptensor_hash_item_t)

        return table

    def sptensor_hash_set(self, index, value):
        print('to be implemented')

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
