"""
Copyright (C) 2017 João Barroca <joao.barroca@tecnico.ulisboa.pt>

This program is free software: you can redistribute it and/or modify it under the terms of the GNU General Public License as published
by the Free Software Foundation, either version 3 of the License, or (at your option) any later version.

This program is distributed in the hope that it will be useful, but WITHOUT ANY WARRANTY; without even the implied warranty of 
MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE. See the GNU General Public License for more details.

You should have received a copy of the GNU General Public License along with this program. If not, see <http://www.gnu.org/licenses/>.
"""

# General Problem Formulation
class GeneralProblem:
    # Problem initialization with initialState, goal state and initial cost.
    def __init__(self, initialState, goalState, pathCost):
        self.initialState = initialState
        self.goalState = goalState
        self.pathCost = pathCost
    # General function to read the useful data for the problem.
    # it can be read from a file or defined directly here.
    def readData(self):
        pass
    # General function to choose the possible actions in a certain state.
    # Return a list of actions.
    def chooseActions(self, state):
        pass
    # General function that represents the transition model of the state space of the problem.
    # Return the successors - a list of dict with the following keys: (state, action, g, h).
    def transitionModel(self, action):
        pass
    # General function that checks if a node has a goal state.
    # Return True or False.
    def goalState(self, node):
        pass
    # General function to compute a heuristic based on the current state.
    # Return the value of h (if we want to use uninformed search, return h=0).
    def heuristic(self, state):
        pass
    # General function that checks if two nodes have the same state (useful for frontier and explored set checking)
    # Return True or False.
    def equalState(self, node1, node2):
        pass
    # General function to write the solution of the problem in terminal and file.
    # it also writes the number of iterations, generated nodes, frontier size and the time to solve the problem.
    def writeSolution(self, file, iteration, nodesGenerated, frontierSize, startTime, solution):
        pass

# Expands the node and gets all the child nodes.
# Using the problem transition model, we get the successors.
# The successors must be a dict with the following keys: (state, action, g, h).
# Then we create the child nodes with these successors.
# Return the child nodes - a list of dict with the following keys: (state, parent, action, g, f)
def childNodesGetter(problem, parent, strategy):
    childNodes = []
    # Get the successors from the problem transition model of the current state
    successors = problem.transitionModel(parent['state'])
    for successor in successors:
        # For each successor, create a child node with the state, nodeparent, the action that was perfomed to get to its state and the path cost
        childNode = {'state': successor['state'], 'parent': parent, 'actions': successor['action'], 'g': (successor['g'] + parent['g']), 'f': successor['g'] + parent['g'] + successor['h']}
        childNodes.append(childNode)
    return childNodes

# Checks if the child node is in the frontier.
# Return True or False
def inFrontier(problem, childNode, frontier):
    for node in frontier:
        # Checks from every node in the frontier if the child node has the same state
        if problem.equalState(node, childNode) is True:
            if node['f'] <= childNode['f']:
                return True
            # If the node in the frontier has a bigger path cost, the remove that node from the frontier
            elif node['f'] > childNode['f']:
                frontier.remove(node)
    # The return False will allow the ugs algortihm to add the child node to the frontier
    return False

# Checks if the child node in in the explored list.
# Return True or False
def inExploredList(problem, childNode, exploredList):
    for node in exploredList:
        # Check if there is already a node with the same state that was explored
        if problem.equalState(node, childNode) is True:
            return True
    # The return False will allow the ugs algortihm to add the child node to the frontier
    return False

# Executes the "backtracking of actions" that lead to the node with the goal state.
# Return the ordered sequence of actions.
def execute(nodeGoal):
    # When a solution if found, we have to perform the back tracking of the actions performed that get us to this goal state
    sequence = [nodeGoal['actions']]
    parentNode = nodeGoal['parent']
    while(parentNode):
        if (parentNode['actions']):
            sequence.extend([parentNode['actions']])
        parentNode = parentNode['parent']
    return [sequence[::-1], nodeGoal['g']]

# Shows the node being explored, the frontier size and number of iterations.
def gsDebug(iteration, node, frontier):
    print('\n\nITERATION', iteration)
    print('\nEXPLORED NODE', (node['state'], node['f'], node['g']))
    print('\nFRONTIER SIZE', len(frontier))
