# -*- coding: utf-8 -*-
"""
Created on Fri Oct 20 2017
@author: Barroca
"""
# Importing the libraries
from operator import itemgetter
from debug import *

def SEARH(problem, strategy):
    node = {'state': problem.initialState, 'parent': [], 'actions': [], 'pathCost': 0}
    frontier = [node]
    exploredSet = []
    iteration = 1
    while(1):
        # When there are no more nodes to explore and we didn't found a solution yet,
        # return Failure
        if not frontier:
            return None
        # Chooses the next node to explore from frontier using the choosen strategy
        node = leafNode(strategy, frontier)
        # Check for solution before expanding the initial node and if its a goal state,
        # executes the solution
        if solution(node, problem.goal):
            return execute(node), iteration
        # Debugging process
        debugGraphSearch(iteration, node, frontier)
        # Adds the node to the explored set
        exploredSet.append(node)
        childNodes = childNodesGetter(problem, node)
        for child in childNodes:
            if solution(child, problem.goal):
               return execute(child), iteration
            if not inExploredList(child, exploredSet) and not inFrontier(child, frontier):
                frontier.append(child)
        iteration+=1

def leafNode(strategy, frontier):
    if strategy is 'FIFO':
        return frontier.pop(0);
    elif strategy is 'LIFO':
        return frontier.pop();
    elif strategy == 'uniformCost':
        frontier.sort(key = itemgetter('pathCost'))
        return frontier.pop(0)

def childNodesGetter(problem, parent):
    childNodes = []
    successors = problem.transitionModel(parent['state'])
    for successor in successors:
        childNode = {'state': successor[0], 'parent': parent, 'actions': successor[1], 'pathCost': (successor[2] + parent['pathCost'])}
        childNodes.append(childNode)
    return childNodes

def inFrontier(childNode, frontier):
    for node in frontier:
        if set(node['state'][0]) == set(childNode['state'][0]) and set(node['state'][1]) == set(childNode['state'][1]):
            if node['pathCost'] <= childNode['pathCost']:
                return True
            elif node['pathCost'] > childNode['pathCost']:
                frontier.remove(node)
    return False

def inExploredList(childNode, exploredList):
    for node in exploredList:
        if set(node['state'][0]) == set(childNode['state'][0]) and set(node['state'][1]) == set(childNode['state'][1]):
            return True
    return False

def solution(node, goal):
    if set(node['state'][0]) == goal:
        return True
    return False

def execute(node):
    sequence = [node['actions']]
    parentNode = node['parent']
    while(parentNode):
        if (parentNode['actions']):
            sequence.extend([parentNode['actions']])
        parentNode = parentNode['parent']
    return [sequence[::-1], node['pathCost']]
