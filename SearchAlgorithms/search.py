"""
Copyright (C) 2017 João Barroca <joao.barroca@tecnico.ulisboa.pt>

This program is free software: you can redistribute it and/or modify it under the terms of the GNU General Public License as published
by the Free Software Foundation, either version 3 of the License, or (at your option) any later version.

This program is distributed in the hope that it will be useful, but WITHOUT ANY WARRANTY; without even the implied warranty of 
MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE. See the GNU General Public License for more details.

You should have received a copy of the GNU General Public License along with this program. If not, see <http://www.gnu.org/licenses/>.
"""

# Importing the libraries
from domainIndependent import *
from operator import itemgetter
import numpy as np
import itertools
import time

# General Graphic Search (with goal state verification only after choosing a leaf node!)
def gs(problem, strategy):
    node = {'state': problem.initialState, 'parent': [], 'actions': [], 'g': 0, 'f': 0}
    frontier = [node]
    exploredSet = []
    iterCounter = itertools.count(start = 0)
    nodesCounter = itertools.count(start = 1)
    iteration = 0
    generatedNodes = 1
    while True:
        # when there are no more nodes to explore and we didn't found a solution yet, return Failure
        if not frontier:
            iteration = next(iterCounter)
            return None, iteration, len(frontier), generatedNodes
        # chooses the node with the lowest cost
        # first we sort by max and then we take the last element of the list
        # this allow us to choose the vertice with the last lowest cost that was
        # appended to list (in case of ties)
        sortedFrontier = sorted(frontier, key = itemgetter('f'), reverse = True)
        node = sortedFrontier[-1]
        # and remove it from the frontier
        frontier.remove(node)
        # checks if the chosen node its a goal state before expand it
        if problem.goalState(node) is True:
            iteration = next(iterCounter)
            return execute(node), iteration, len(frontier), generatedNodes
        iteration = next(iterCounter)
        # Debugging process
        #gsDebug(iteration, node, frontier)
        # adds the node being explored to the explored set
        exploredSet.append(node)
        # expand the node and get the child nodes
        childNodes = childNodesGetter(problem, node, strategy)
        for child in childNodes:
            generatedNodes = next(nodesCounter)
            # checks if the child node has already been explored or if it is already in the frontier
            if not inExploredList(problem, child, exploredSet) and not inFrontier(problem, child, frontier):
                frontier.append(child)
