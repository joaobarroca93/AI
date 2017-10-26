"""
Copyright (C) 2017 João Barroca <joao.barroca@tecnico.ulisboa.pt>

This program is free software: you can redistribute it and/or modify it under the terms of the GNU General Public License as published
by the Free Software Foundation, either version 3 of the License, or (at your option) any later version.

This program is distributed in the hope that it will be useful, but WITHOUT ANY WARRANTY; without even the implied warranty of 
MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE. See the GNU General Public License for more details.

You should have received a copy of the GNU General Public License along with this program. If not, see <http://www.gnu.org/licenses/>.
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
