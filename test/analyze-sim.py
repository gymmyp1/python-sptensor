# This program analyzes the output from hashsim.py.
import sys
import matplotlib.pyplot as plt

# load up the data
data = []
with open(sys.argv[1], 'r') as file:
    # get the number of buckets
    nbuckets = file.readline().split('\t')
    nbuckets = int(nbuckets[1])

    # throw away the header line
    file.readline()

    # process the rest
    for line in file:
        line = line.split('\t')
        data.append(tuple(int(i) for i in line))

# create the counts array
counts = [0] * nbuckets
collisions = 0
entries = len(data)
for datum in data:
    index = datum[-1]
    counts[index] += 1
    if counts[index] > 1:
        collisions += 1

# compute the collision percent
colrate = collisions / entries * 100

# plot the distribution of entries
fig, ax = plt.subplots()
ax.set_title("Distribution of Hash Keys")
ax.plot(range(nbuckets), counts)
ax.set_xlabel('Bucket')
ax.set_ylabel('Entry Count')
report = '\n'.join((
    'Buckets: %d' % (nbuckets),
    'Entries: %d' % (entries,),
    'Collisions: %d' % (collisions,),
    'Collision Rate: %.2f%%' % (colrate,)
))
ax.text(0.95, 0.95, 
        report, 
        ha='right', va='top',
        transform=ax.transAxes,
        bbox=dict(boxstyle='round', facecolor='wheat'))
plt.show()