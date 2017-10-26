"""
Copyright (C) 2017 João Barroca <joao.barroca@tecnico.ulisboa.pt>

This program is free software: you can redistribute it and/or modify it under the terms of the GNU General Public License as published
by the Free Software Foundation, either version 3 of the License, or (at your option) any later version.

This program is distributed in the hope that it will be useful, but WITHOUT ANY WARRANTY; without even the implied warranty of 
MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE. See the GNU General Public License for more details.

You should have received a copy of the GNU General Public License along with this program. If not, see <http://www.gnu.org/licenses/>.
"""

# Creates a file to write the data of the performed tests
try:
    file = open("AI.txt","a")
except IOError:
    print("Error creating file")

# Importing the libraries
from problemFormulation import Problem
from operator import itemgetter
import datetime
import time
import sys
import search
import debug

# Process the commands reveiced throught terminal
commands = sys.argv
if len(commands) != 3 or commands[1] != '-i' and commands[1] != '-u':
    sys.exit("CommandError: command line must be solver.py -i(informed)/-u(uninformed) textfilename.txt")

# Imports the data from text file
verticesDict = {}
launchesDict = {}
verticesMapping = {}
launches = []
edges = []
epochDate = datetime.date(1900, 1, 1)
# Reads the data from file
with open(commands[2]) as fh:
    for line in fh:
        #if line[0] == 'V':
        if 'V' in line[0]:
            # Dict of the vertices whoose keys are the available vertices and values are their weight
            verticesDict[line.split()[0]] = [float(line.split()[1])]
        elif 'E' in line:
            # Edges
            edges.append(line.split()[1:3])
        elif 'L' in line:
            # Delta is the time (in days) since the epoch (1/1/1900) till the launch day
            # Since a variable in python can have 64bits, we dont have to be worry about overflows
            delta = datetime.date(int(line.split()[1][4:9]), int(line.split()[1][2:4]), int(line.split()[1][0:2])) - epochDate
            launches.append([delta.days, line.split()[1], float(line.split()[2]), float(line.split()[3]), float(line.split()[4])])
            # Sorts launches by date
            launches.sort(key = itemgetter(0))
    
    # Creates  a dict of the launches whoose keys are the available launches (already orderer by date) with a list containing
    # ['date', maximum payload, fixed cost, variable cost] as valors
    counter = 1
    for launch in launches:
        launchesDict['L'+str(counter)] = launch[1:5]
        counter = counter + 1
    # Creates a dict whoose keys are the available vertices with all the vertices that can connect with as valors
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

# Checks the feasibility of the data
# Does all the vertices have connections?
if not [value for value in verticesMapping.values()]:
    sys.exit("Error: insufficient number of edges")
# Is the sum of the maximum payload of the launches bigger that the sum of the weight of the vertices ?

# Problem formulaion
problem = Problem(verticesDict, launchesDict, verticesMapping)

# Choosing strategy
STRATEGY = 'uniformCost'

start = time.time()
# Uninformed Search algorithm
solution, iteration = search.ugs(problem, STRATEGY)

# Writing parameters to the file and terminal
file.write(commands[2] + "\t" + STRATEGY + "\n")
print('\n\n\nEXECUTION TIME: ', time.time()-start)
file.write("iterations\t" + str(iteration) + "\n")
file.write("execution time\t" + str(time.time()-start) + "\n")

# Solution print for file and terminal
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

# Closes the file
file.close()
