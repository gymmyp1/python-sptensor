# This program analyzes the output from hashsim.py.
import sys
import matplotlib.pyplot as plt
import math
import numpy as np

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

#Trying to create a heatmap style plot

# Define numbers of generated data points and bins per axis.
N_numbers = nbuckets
N_bins = 100

# Generate 2D normally distributed numbers.
sn = math.sqrt(nbuckets)
floor = math.floor(sn)
ceil = math.ceil(sn)
padding =  floor * ceil - len(counts)
if padding > 0:
    counts = counts + [0] * padding
xy = np.reshape(counts, (floor,ceil))
#new = np.array_split(xy,2)
#??
# Construct 2D histogram from data using the 'plasma' colormap
#plt.hist2d(x, y, bins=N_bins, normed=False, cmap='plasma')
plt.imshow(xy, cmap='plasma', interpolation='nearest')

# Plot a colorbar with label.
cb = plt.colorbar()
cb.set_label('Number of entries')

# Add title and labels to plot.
plt.title('Heatmap of 2D normally distributed data points')
plt.xlabel('x axis')
plt.ylabel('y axis')

# Show the plot.
plt.show()

# plot the distribution of entries
'''fig, ax = plt.subplots()
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
plt.show()'''
