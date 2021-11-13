import os, sys

class csf_node:
    def __init__(self, value):
        
        ## pointer structure for each subtree. 
        self.children = []

        ## value of each node
        self.value = value


    def add_child(self, value):
        node = csf_node(value)
        self.children.append(node)

    def find(self, val):
        for child in self.children:
            if child.value == val:
                return child

        return -1

    def add_nnz(self, idx, nnz):
        node = self
        while bool(idx) and node.find(idx[0]) != -1:
            node = node.find(idx[0])
            idx.pop(0)

        while bool(idx):
            node.add_child(idx[0])
            node = node.find(idx[0])
            idx.pop(0)
        
        node.add_child(nnz)
    
    def print(self, level=0):
        print(' ' * level + str(self.value))
        for child in self.children:
            child.print(level+1)


class splatt_csf:
    def __init__(self, fname):

        # open file in tensor format for reading
        tensorfile = open(os.path.join(sys.path[0], fname), "r")

        self.nmodes = 0
        self.nnz = 0
        self.dims = []

        self.root = csf_node(-1)
        
        for line in tensorfile:
            if line.startswith('#'):
                continue

            nums = line.split()
            nonzero = nums.pop()

            self.nnz += 1

            
            current_idx = [int(num) for num in nums]

            if self.nmodes == 0:
                self.nmodes = len(nums)
                self.dims = current_idx.copy()
                #print('number of modes: ' + str(self.nmodes))
                #print('starting dims: ' + ' '.join(map(str, self.dims)))
            else:

                #print('current indices: ' + str(current_idx))
                #print('current dims: ' + str(self.dims))
                for i in range(self.nmodes):
                    #print('i is ' + str(i))
                    self.dims[i] = self.dims[i] if self.dims[i] > current_idx[i] else current_idx[i]


            #print('indices: ' + ' '.join(map(str, nums)))
            #print('value: ' + str(nonzero))

            self.root.add_nnz(current_idx, nonzero)

        tensorfile.close()

        #print('final dims: ' + ' '.join(map(str, self.dims)))

        #print('reading through tree: ')
        #self.root.print()

#if __name__ == '__main__':

#    csf = splatt_csf('test.txt')