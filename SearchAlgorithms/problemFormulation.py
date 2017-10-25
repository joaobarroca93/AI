# -*- coding: utf-8 -*-
"""
Created on Fri Oct 20, 2017
@author: João Barroca <joao.barroca@tecnico.ulisboa.pt>
"""

# Importing the libraries
from debug import *
import copy
import time

# Problem class
class Problem():
    # Problem initialization
    def __init__(self, verticesDict, launchesDict, verticesMapping):
        self.verticesDict = verticesDict
        self.launchesDict = launchesDict
        self.verticesMapping = verticesMapping
        self.initialState = [[],[],0]
        self.goal = set(verticesDict.keys())
        self.stepCost = 0
        #debugProbleInit(self.initialState, self.goal, self.stepCost, self.actions)

    # Chooses an action based on the current state
    def chooseAction(self, state):
        actions = []
        if not state[1]:
            actions.extend(list(self.launchesDict.keys()))
        else:
            if not state[0]:
                actions.extend(list(self.verticesDict.keys()))
                index = list(self.launchesDict.keys()).index(state[1][-1])
                actions.extend(list(self.launchesDict.keys())[index+1:])
            else:
                for vertice in state[0]:
                    actions.extend(self.verticesMapping[vertice])
                    index = list(self.launchesDict.keys()).index(state[1][-1])
                    actions.extend(list(self.launchesDict.keys())[index+1:])
        actions = set(actions) - set(list(state[0])) - set(list(state[1]))
        actions = list(actions)
        return actions

    # Applies the actions to the state and get the resulted states
    def transitionModel(self, state):
        successors = []
        actions = self.chooseAction(state)
        for action in actions:
            loadWeight = state[2]
            newState = copy.deepcopy(state)
            if action[0] == 'V':
                if loadWeight + self.verticesDict[action][0] > self.launchesDict[state[1][-1]][1]:
                    cost = 0
                else:
                    newState[0].extend([action])
                    loadWeight += self.verticesDict[action][0]
                    cost = self.verticesDict[action][0] * self.launchesDict[state[1][-1]][3]
            elif action[0] == 'L':
                newState[1].extend([action])
                cost = self.launchesDict[action][2]
                loadWeight = 0
            newState[2] = loadWeight
            #debugTransitionModel(state, action, newState, cost)
            successors.append([newState, action, cost])
        return successors
