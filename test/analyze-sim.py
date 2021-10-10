# This program analyzes the output from hashsim.py.
import sys
import matplotlib.pyplot as plt
from matplotlib.colors import LinearSegmentedColormap
import math
import numpy as np
from scipy import stats
import seaborn as sns

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

sum = 0
count = 0
max = 0

nzcounts=[]
# Average the # of non-zero xounts in the array / number of non-zeroes
for i in range(len(counts)):
	if counts[i] != 0:
		sum = sum + counts[i]
		count = count + 1
		nzcounts.append(counts[i])
		if counts[i] > max:
			max = counts[i]

avg = sum/count
stdev = np.std(nzcounts)
mode = stats.mode(nzcounts)
median = np.median(nzcounts)

print("avg probe depth: ", avg)
print('max probe depth: ', max)
print('standard deviation:', stdev)
print('mode:', mode)
print('median:', median)

sns.kdeplot(nzcounts)

# Create heatmap style plot

# Define numbers of generated data points and bins per axis.
N_numbers = nbuckets
N_bins = 100

# Generate 2D version of the counts
sn = math.sqrt(nbuckets)
floor = math.floor(sn)
ceil = math.ceil(sn)
padding =  floor * ceil - len(counts)
if padding > 0:
    counts = counts + [0] * padding
xy = np.reshape(counts, (floor,ceil))

#
fig, ax = plt.subplots()

#display the heatmap
#clist = [(0, '#000000'), (1/max, '#00ff00'), (0.5,'#c1dd21'), (1.0,'#ff0000')]
clist = [(0, '#000000'), (1/max, '#ffffff'), (1.0,'#ff0000')]
bucket_cmap = LinearSegmentedColormap.from_list('bucket_cmap', clist, N=max)
img = ax.imshow(xy, cmap=bucket_cmap, interpolation='nearest')
ax.set_xticks([])
ax.set_yticks([])

# Plot a colorbar with label.
cb = plt.colorbar(img, ax=ax)
cb.set_label('Number of Keys in Bucket')

# Add title and labels to plot.
ax.set_title('Heatmap of Hash Function (row-major)')

# The text report
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

# Show the plot.
plt.show()
