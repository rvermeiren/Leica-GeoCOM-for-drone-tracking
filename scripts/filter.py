#!/usr/bin/python

import re
import sys

def filter_text(file):
	""" Read a text file which contain coordinates in
	the format (x,y,z) and puts them in a list of tuples.
	"""
	points = []
	with open(sys.argv[1]) as document:
		for line in document:
			regex = re.compile("\(.+\)").findall(line)
			for match in regex:
				coordinates = match.replace("(","").replace(")","").split(",")
				print(match)
				#points.append((float(coordinates[0]), float(coordinates[1]), float(coordinates[2])))
	return points

if len(sys.argv) != 2:
	print("Usage : python3 filter.py <data_file>")
	sys.exit(-1)
filter_text(sys.argv[1])