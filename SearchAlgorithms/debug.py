# -*- coding: utf-8 -*-
"""
Created on Fri Oct 20, 2017
@author: João Barroca <joao.barroca@tecnico.ulisboa.pt>
"""

def debugData(verticesDict, launchesDict, verticesMapping):
    print('\n=================================== LAUNCHES AVAILABLE')
    for key in launchesDict.keys():
        print('%s \t %s %s %s %s'
        % (key, launchesDict[key][0], launchesDict[key][1], launchesDict[key][2], launchesDict[key][3]))
    print('\n=================================== MODULES')
    for key in verticesDict.keys():
        print('%s \t %s' % (key, verticesDict[key][0]))
    print('\n=================================== CONNECTIONS')
    for key in verticesMapping.keys():
        print('%s \t %s' % (key, ' '.join(verticesMapping[key])))

def debugProbleInit(initialState, goal, pathCost, actions):
    print('\n=================================== PROBLEM')
    print('InitialState: %s' % initialState)
    print('Goal: %s' % goal)
    print('Cost: %s' % pathCost)
    print('Actions: %s' % actions)

def debugGraphSearch(iteration, node, frontier):
    print('\n\nITERATION', iteration)
    print('\nEXPLORED NODE', (node['state'], node['pathCost']))
    print('\nFRONTIER SIZE', len(frontier))

def debugTransitionModel(state, action, newState, cost):
    print('\nSTATE: ', state)
    print('ACTION: ', action)
    print('RESULTED STATE: ', newState)
    print('COST: ', cost)
