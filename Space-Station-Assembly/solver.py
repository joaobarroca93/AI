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
from domainDependent import Problem
from search import *
import time
import sys

# Problem formulation and domain dependent functions
problem = Problem(sys.argv)

startTime = time.time()
# Graph Search algorithm
solution, iteration, frontierSize, generatedNodes = gs(problem, problem.strategy)

problem.writeSolution(file, iteration, frontierSize, generatedNodes, startTime, solution)
file.close()
