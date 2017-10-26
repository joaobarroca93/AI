"""
Copyright (C) 2017 João Barroca <joao.barroca@tecnico.ulisboa.pt>

This program is free software: you can redistribute it and/or modify it under the terms of the GNU General Public License as published
by the Free Software Foundation, either version 3 of the License, or (at your option) any later version.

This program is distributed in the hope that it will be useful, but WITHOUT ANY WARRANTY; without even the implied warranty of 
MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE. See the GNU General Public License for more details.

You should have received a copy of the GNU General Public License along with this program. If not, see <http://www.gnu.org/licenses/>.
"""

# Importing the libraries
from operator import itemgetter
from debug import *

# Uninformed Graphic Search
def ugs(problem, strategy):
    node = {'state': problem.initialState, 'parent': [], 'actions': [], 'pathCost': 0}
    frontier = [node]
    exploredSet = []
    iteration = 1
    while(1):
        # When there are no more nodes to explore and we didn't found a solution yet, return Failure
        if not frontier:
            return None
        # Chooses the next node to explore from frontier using the choosen strategy('LIFO', 'FIFO' or 'uniformCost')
        node = leafNode(strategy, frontier)
        # Check for solution before expanding the initial node and if its a goal state, executes the solution
        if solution(node, problem.goal):
            return execute(node), iteration
        # Debugging process
        ugsDebug(iteration, node, frontier)
        # Adds the node being explored to the explored set
        exploredSet.append(node)
        # Expand the node and get the child nodes
        childNodes = childNodesGetter(problem, node)
        for child in childNodes:
            # For each expanded node (child), checks if it represents a goal state
            if solution(child, problem.goal):
               return execute(child), iteration
           # If not a node with a goal state, then check if it is already been explored or if it is already in the frontier, adding it to the frontier if not
            if not inExploredList(child, exploredSet) and not inFrontier(child, frontier):
                frontier.append(child)
        iteration+=1

# Chooses a leaf node to expand
def leafNode(strategy, frontier):
    # FIFO strategy pops from the frontier the first node (the oldest node added)
    if strategy is 'FIFO':
        return frontier.pop(0);
    # LIFO strategy pops from the frontier the last node (the newest node added)
    elif strategy is 'LIFO':
        return frontier.pop();
    # uniformCost strategy orders the frontier for pathCost (lowest path cost comes first) and pops the first node (the one with the lowest pathCost)
    elif strategy == 'uniformCost':
        frontier.sort(key = itemgetter('pathCost'))
        return frontier.pop(0)

# Expands the node and gets all the child nodes
def childNodesGetter(problem, parent):
    childNodes = []
    # Get the successors from the problem transition model of the current state
    successors = problem.transitionModel(parent['state'])
    for successor in successors:
        # For each successor, create a child node with the state, nodeparent, the action that was perfomed to get to its state and the path cost
        childNode = {'state': successor[0], 'parent': parent, 'actions': successor[1], 'pathCost': (successor[2] + parent['pathCost'])}
        childNodes.append(childNode)
    return childNodes

# Checks if the child node is in the frontier
def inFrontier(childNode, frontier):
    for node in frontier:
        # Checks from every node in the frontier if the child node has the same state
        if set(node['state'][0]) == set(childNode['state'][0]) and set(node['state'][1]) == set(childNode['state'][1]):
            # If it has the same state, checks if the node in the frontier has a lower or equal path cost
            if node['pathCost'] <= childNode['pathCost']:
                return True
            # If the node in the frontier has a bigger path cost, the remove that node from the frontier
            elif node['pathCost'] > childNode['pathCost']:
                frontier.remove(node)
    # The return False will allow the ugs algortihm to add the child node to the frontier
    return False

# Checks if the child node in in the explored list
def inExploredList(childNode, exploredList):
    for node in exploredList:
        # Check if there is already a node with the same state that was explored
        if set(node['state'][0]) == set(childNode['state'][0]) and set(node['state'][1]) == set(childNode['state'][1]):
            return True
    # The return False will allow the ugs algortihm to add the child node to the frontier
    return False

# Checks if the state of the node is a goal state
def solution(node, goal):
    # If the state of the node is a goal state, then we found a solution
    if set(node['state'][0]) == goal:
        return True
    return False

# Executes the "backtracking of actions" that lead to the node with the goal state
def execute(node):
    # When a solution if found, we have to perform the back tracking of the actions performed that get us to this goal state
    sequence = [node['actions']]
    parentNode = node['parent']
    while(parentNode):
        if (parentNode['actions']):
            sequence.extend([parentNode['actions']])
        parentNode = parentNode['parent']
    return [sequence[::-1], node['pathCost']]
