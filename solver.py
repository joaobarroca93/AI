# -*- coding: utf-8 -*-
"""
Created on Fri Oct 20 21:24:03 2017

@author: Barroca
"""

# Importing the libraries
from problemFormulation_NEW import Problem
from debug import *
from operator import itemgetter
import datetime
import time
import sys
import search

# Importing the data from text file
verticesDict = {}
launchesDict = {}
verticesMapping = {}
launches = []
edges = []
epochDate = datetime.date(1900, 1, 1)
# Reading the data
with open('simple.txt') as fh:
    for line in fh:
        #if line[0] == 'V':
        if 'V' in line[0]:
            verticesDict[line.split()[0]] = [float(line.split()[1])]
        elif 'E' in line:
            edges.append(line.split()[1:3])
        elif 'L' in line:
            delta = datetime.date(int(line.split()[1][4:9]), int(line.split()[1][2:4]), int(line.split()[1][0:2])) - epochDate
            launches.append([delta.days, line.split()[1], float(line.split()[2]), float(line.split()[3]), float(line.split()[4])])
            launches.sort(key = itemgetter(0))
    counter = 1
    for launch in launches:
        launchesDict['L'+str(counter)] = launch[1:5]
        counter = counter + 1

    for edge in edges:
        if edge[0] in verticesMapping:
            verticesMapping[edge[0]].append(edge[1])
        elif not edge[0] in verticesMapping:
            verticesMapping[edge[0]] = [edge[1]]
        if edge[1] in verticesMapping:
            verticesMapping[edge[1]].append(edge[0])
        elif not edge[1] in verticesMapping:
            verticesMapping[edge[1]] = [edge[0]]
# For debugging the data available
#debugData(verticesDict, launchesDict, verticesMapping)

# Problem formulaion
problem = Problem(verticesDict, launchesDict, verticesMapping)

start = time.time()
# Search algorithm
solution = search.GRAPH_SEARH(problem, 'uniformCost')
print('\n\n\nEXECUTION TIME: ', time.time()-start)

# Solution print for serial
if solution:
    print("\n\nSOLUTION")
    for eachStep in solution[0]:
        if 'L' in eachStep:
            print()
            print(problem.launchesDict[eachStep][0], end=' ')
        elif 'V' in eachStep:
            print(eachStep, end=' ')
    print()
    print(solution[1])
else:
    print("\n\nNO SOLUTION\n", 0)
