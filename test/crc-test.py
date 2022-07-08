import binascii

idx = [1,5,2]

# Converting integer list to string list
s = [str(i) for i in idx]
# Join list items using join()
m = ''.join(s)
text_bytes = bytes(m,'utf-8')
hash = binascii.crc32(text_bytes)
k = int(hash) % nbuckets


crc(idx)
