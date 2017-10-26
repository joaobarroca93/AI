"""
Copyright (C) 2017 João Barroca <joao.barroca@tecnico.ulisboa.pt>

This program is free software: you can redistribute it and/or modify it under the terms of the GNU General Public License as published
by the Free Software Foundation, either version 3 of the License, or (at your option) any later version.

This program is distributed in the hope that it will be useful, but WITHOUT ANY WARRANTY; without even the implied warranty of 
MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE. See the GNU General Public License for more details.

You should have received a copy of the GNU General Public License along with this program. If not, see <http://www.gnu.org/licenses/>.
"""

# Importing the libraries
from debug import *
import copy

# Problem class
class Problem():
    # Problem initialization
    # - verticesDict is a dict whoose keys are the available vertices with their weight as valors
    # - launchesDict is a dict whoose keys are the available launches (already orderer by date) with a list containing
    # ['date', maximum payload, fixed cost, variable cost] as valors
    # - verticesMapping is a dict whoose keys are the available vertices with all the vertices that can connect with as valors
    # - our INITIAL STATE will be a list of [[vertices],[launches], loadWeight]
    # The vertices will be the ones that are already on orbit or that were loaded to the current launch
    # the launches will be the ones that were already performed or the launch that is being loaded(it is always the last one)
    # the loadWeight is the current weight of the launch (this allows me to keep track of the weight, making the constrain of weight more easy)
    # - the GOAL of the problem is to have all the vertices in orbit (in the state)
    # - our ACTIONS will be to choose a vertice or a launch
    # - our STEP COST will be the fixed cost (when we choose a launch) and a variable cost*weight (when we choose a vertice)
    def __init__(self, verticesDict, launchesDict, verticesMapping):
        self.verticesDict = verticesDict
        self.launchesDict = launchesDict
        self.verticesMapping = verticesMapping
        self.initialState = [[],[],0]
        self.goal = set(verticesDict.keys())

    # Chooses an action based on the current state
    def chooseAction(self, state):
        actions = []
        # If there is not any launch chosen yet, chooses one of the launches
        if not state[1]:
            actions.extend(list(self.launchesDict.keys()))
        else:
            # If there is not any vertice in orbit or being loaded to launch, it will choose a vertice from all of the vertices or a launch
            # different from the ones already performed
            if not state[0]:
                actions.extend(list(self.verticesDict.keys()))
                index = list(self.launchesDict.keys()).index(state[1][-1])
                actions.extend(list(self.launchesDict.keys())[index+1:])
            # If there are already vertices in orbit or in the launch being loaded, it will choose a vertice from the ones that connect to
            # those already there or in orbit
            else:
                for vertice in state[0]:
                    actions.extend(self.verticesMapping[vertice])
                    index = list(self.launchesDict.keys()).index(state[1][-1])
                    actions.extend(list(self.launchesDict.keys())[index+1:])
        # Little "trick" to remove from the possible actions, the ones that are equal to the ones already performed
        actions = set(actions) - set(list(state[0])) - set(list(state[1]))
        actions = list(actions)
        #print('\nACTIONS: ', actions)
        return actions

    # Applies the actions to the state and get the resulted states (successors)
    def transitionModel(self, state):
        successors = []
        # Choose all possible actions for the state
        actions = self.chooseAction(state)
        for action in actions:
            # loadWeight is the current weight of the launch being loaded
            loadWeight = state[2]
            # Copy the state by valor (not reference)
            newState = copy.deepcopy(state)
            # If our action is to choose a vertice
            if action[0] == 'V':
                # Do nothing if the chosen vertice weight will exceed maximum payload and set a null cost
                if loadWeight + self.verticesDict[action][0] > self.launchesDict[state[1][-1]][1]:
                    cost = 0
                # Adds the vertice to the state and refresh the new loadWeight (adds the chosen vertice weight) and
                # the action cost (vertice weight times the variable cost of the launch being loaded)
                else:
                    newState[0].extend([action])
                    loadWeight += self.verticesDict[action][0]
                    cost = self.verticesDict[action][0] * self.launchesDict[state[1][-1]][3]
            # If our action is to choose a launch, adds the launch to the state and refresh the loadWeight(will be 0 because there is a new launch to be loaded)
            # and cost (fixed cost of the chosen launch)
            elif action[0] == 'L':
                newState[1].extend([action])
                cost = self.launchesDict[action][2]
                loadWeight = 0
            # Adds the new loadWeight to the state
            newState[2] = loadWeight
            #debugTransitionModel(state, action, newState, cost)
            # Adds to the successors the new state the action performed and the action cost
            successors.append([newState, action, cost])
        #print('SUCCESSORS: ', successors)
        return successors
