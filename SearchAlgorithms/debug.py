# -*- coding: utf-8 -*-
"""
Created on Fri Oct 20, 2017
@author: João Barroca <joao.barroca@tecnico.ulisboa.pt>
"""

# shows the data processed from the read file
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

# shows the node being explored, the frontier size and number of iterations
def ugsDebug(iteration, node, frontier):
    print('\n\nITERATION', iteration)
    print('\nEXPLORED NODE', (node['state'], node['pathCost']))
    print('\nFRONTIER SIZE', len(frontier))

# shows the state, the action that will be performed, the resulted state and the action cost
def debugTransitionModel(state, action, newState, cost):
    print('\nSTATE: ', state)
    print('ACTION: ', action)
    print('RESULTED STATE: ', newState)
    print('COST: ', cost)
