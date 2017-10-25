# -*- coding: utf-8 -*-
"""
Created on Fri Oct 20, 2017
@author: João Barroca <joao.barroca@tecnico.ulisboa.pt>
"""

# Creating file
try:
    file = open("AI.txt","a")
except IOError:
    print("Error creating file")

# Importing the libraries
from problemFormulation import Problem
from debug import *
from operator import itemgetter
import datetime
import time
import sys
import search

# Processing the commands reveiced throught terminal
commands = sys.argv
if len(commands) != 3 or commands[1] != '-i' and commands[1] != '-u':
    sys.exit("CommandError: command line must be solver.py -i(informed)/-u(uninformed) textfilename.txt")

# Importing the data from text file
verticesDict = {}
launchesDict = {}
verticesMapping = {}
launches = []
edges = []
epochDate = datetime.date(1900, 1, 1)
# Reading the data
with open(commands[2]) as fh:
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

# Feasibility
if not [value for value in verticesMapping.values()]:
    sys.exit("Error: insufficient number of edges")

# Problem formulaion
problem = Problem(verticesDict, launchesDict, verticesMapping)

# Choosing strategy
STRATEGY = 'uniformCost'

start = time.time()
# Search algorithm
solution, iteration = search.SEARH(problem, STRATEGY)

# Writing parameters to file
file.write(commands[2] + "\t" + STRATEGY + "\n")
print('\n\n\nEXECUTION TIME: ', time.time()-start)
file.write("iterations\t" + str(iteration) + "\n")
file.write("execution time\t" + str(time.time()-start) + "\n")

# Solution print for serial
if solution:
    file.write("solution\n")
    print("\n\nSOLUTION")
    cost = 0
    for eachStep in solution[0]:
        if 'L' in eachStep:
            if cost:
                print(cost)
                file.write(str(cost) + "\n")
            print(problem.launchesDict[eachStep][0], end=' ')
            file.write(str(problem.launchesDict[eachStep][0]) + "\t")
            cost = problem.launchesDict[eachStep][2]
            varCost = problem.launchesDict[eachStep][3]
        elif 'V' in eachStep:
            print(eachStep, end=' ')
            file.write(str(eachStep) + "\t")
            cost += varCost*problem.verticesDict[eachStep][0]
    print(cost, end='')
    file.write(str(cost) + "\n")
    print()
    print(solution[1])
    file.write(str(solution[1]) + "\n\n")
else:
    print("\n\nNO SOLUTION\n", 0)
    file.write("no solution\n" + str(0)+"\n\n")

file.close()
