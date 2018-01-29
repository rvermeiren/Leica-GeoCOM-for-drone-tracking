#!/usr/bin/python
from mpl_toolkits.mplot3d import Axes3D
import matplotlib.pyplot as plt
import numpy as np
from time import sleep
import sys

# Fixing random state for reproducibility
np.random.seed(19680801)

fig = plt.figure()
ax = fig.add_subplot(111, projection='3d')
ax.plot([0,10],[0,10],[0,5])

ax.set_xlabel('X')
ax.set_ylabel('Y')
ax.set_zlabel('Z')

while True:

	line = sys.stdin.readline()
	if line:
		coordinates = line.replace("(","").replace(")","").split(",")
		#print(coordinates)
		xs = float(coordinates[0])	
		ys = float(coordinates[1])
		zs = float(coordinates[2])
		ax.scatter(xs, ys, zs, c='r', marker='.')
		plt.pause(0.01)
	else:
		#sys.exit(-1)
		sleep(3)

	# For each set of style and range settings, plot n random points in the box
	# defined by x in [23, 32], y in [0, 100], z in [zlow, zhigh].

	# for c, m, zlow, zhigh in [('r', 'o', -50, -25), ('b', '^', -30, -5)]:
	#     xs = randrange(n, 23, 32)
	#     ys = randrange(n, 0, 100)
	#     zs = randrange(n, zlow, zhigh)
	

	#plt.show()