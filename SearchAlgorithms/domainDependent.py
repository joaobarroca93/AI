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
import copy
import datetime
import time

# Problem Formulation
class Problem():
    # - our STATES will be a list of [[vertices],[launches], loadWeight]
    # The vertices will be the ones that are already on orbit or that were loaded to the current launch
    # the launches will be the ones that were already performed or the launch that is being loaded(it is always the last one)
    # the loadWeight is the current weight of the launch (this allows me to keep track of the weight, making the constrain of weight more easy)
    # - the GOAL of the problem is to have all the vertices in orbit (in the state)
    # - our ACTIONS will be to choose a vertice or a launch
    # - our STEP COST will be the fixed cost (when we choose a launch) and a variable cost*weight (when we choose a vertice)
    def __init__(self, commands):
        self.commands = commands
        self.readData()
        self.initialState = [[],[],0]
        self.goal = set(self.verticesDict.keys())

    # Functions that reads the data from the textfile using the commands
    # - verticesDict is a dict whoose keys are the available vertices with their weight as valors
    # - launchesDict is a dict whoose keys are the available launches (already orderer by date) with a list containing
    # ['date', maximum payload, fixed cost, variable cost] as valors
    # - verticesMapping is a dict whoose keys are the available vertices with all the vertices that can connect with as valors
    def readData(self):
        # Process the commands reveiced throught terminal
        if len(self.commands) != 3 or self.commands[1] != '-i' and self.commands[1] != '-u':
            sys.exit("CommandError: command line must be solver.py -i(informed)/-u(uninformed) textfilename.txt")
        self.verticesDict = {}
        self.launchesDict = {}
        self.verticesMapping = {}
        launches = []
        edges = []
        epochDate = datetime.date(1900, 1, 1)
        # Reads the data from file
        with open(self.commands[2]) as fh:
            for line in fh:
                if 'V' in line[0]:
                    self.verticesDict[line.split()[0]] = [float(line.split()[1])]
                elif 'E' in line:
                    edges.append(line.split()[1:3])
                elif 'L' in line:
                    # Delta is the time (in days) since the epoch (1/1/1900) till the launch day
                    # Since a variable in python can have 64bits, we dont have to be worry about overflows
                    delta = datetime.date(int(line.split()[1][4:9]), int(line.split()[1][2:4]), int(line.split()[1][0:2])) - epochDate
                    launches.append([delta.days, line.split()[1], float(line.split()[2]), float(line.split()[3]), float(line.split()[4]), float(line.split()[4]) * float(line.split()[2]) + float(line.split()[3])])
                    launches.sort(key = itemgetter(0))
            counter = 1
            for launch in launches:
                self.launchesDict['L'+str(counter)] = launch[0:6]
                counter = counter + 1
            for edge in edges:
                if edge[0] in self.verticesMapping:
                    self.verticesMapping[edge[0]].append(edge[1])
                elif not edge[0] in self.verticesMapping:
                    self.verticesMapping[edge[0]] = [edge[1]]
                if edge[1] in self.verticesMapping:
                    self.verticesMapping[edge[1]].append(edge[0])
                elif not edge[1] in self.verticesMapping:
                    self.verticesMapping[edge[1]] = [edge[0]]
        # For debugging the data available
        self.debugData()
        # Choosing strategy from commands
        if self.commands[1] == '-i':
            self.strategy = 'informed'
            wait = input("\nTo start Informed Graph Search press any key ...\n")
        if self.commands[1] == '-u':
            self.strategy = 'uninformed'
            wait = input("\nTo start Uninformed Graph Search press any key ...\n")
        # Checks the feasibility of the data
        # Does all the vertices have connections?
        if  len(self.verticesMapping.keys()) < len(self.verticesDict.keys()):
            sys.exit("\n\nProblem not solvable: insufficient number of edges")
        # Is the sum of the maximum payload of the launches bigger that the sum of the weight of the vertices ?

    # Chooses all possible actions based on the current state.
    # When there is not any launch chosen yet, chooses one of the launches. Then, if a launch (or more) is already chosen, and if there are
    # not any vertices in orbit or in the launch being loaded, it will choose one of the vertices.
    # If there are already vertices in orbit or being loaded, we have to choose the vertices that will connect to them, without exceeding the
    # launch maximum payload. It will only choose a new launch if there are not any vertices that will not exceed max payload.
    def chooseActions(self, state):
        actions = []
        vertices = state[0]
        launches = state[1]
        currentWeight = state[2]
        if not launches:
            actions = self.allLaunches(actions)
        else:
            if not vertices:
                actions = self.allVertices(actions)
            else:
                actions = self.allowedVertices(vertices, launches, currentWeight, actions)
                if not actions:
                    actions = self.allowedLaunches(launches, actions)
        """print('\nACTIONS: ', actions)"""
        return actions

    # Chooses all the launches.
    def allLaunches(self, actions):
        actions.extend(list(self.launchesDict.keys()))
        return actions

    # Chooses all the vertices.
    def allVertices(self, actions):
        actions.extend(list(self.verticesDict.keys()))
        return actions

    # Chooses all the vertices that connect with the ones already in orbit or in the launch.
    # Then checks if any of those vertices will exceed maximum payoad, removing them from
    # the actions if true.
    def allowedVertices(self, vertices, launches, currentWeight, actions):
        for vertice in vertices:
            actions.extend(self.verticesMapping[vertice])
        currentLaunchMaxPayload = self.launchesDict[launches[-1]][2]
        for action in copy.deepcopy(actions):
            verticeWeight = self.verticesDict[action][0]
            if currentWeight + verticeWeight > currentLaunchMaxPayload:
                actions.remove(action)
        return list(set(actions) - set(list(vertices)))

    # Chooses all the vertices that will occur after the one already taken.
    def allowedLaunches(self, launches, actions):
        sortedLaunches = [x[0] for x in sorted(self.launchesDict.items(), key=itemgetter(1))]
        index = sortedLaunches.index(launches[-1])
        actions.extend(sortedLaunches[index+1:])
        return actions

    # Transition model of the states of the proble.
    # Applies the actions to the state and get the resulted states (successors).
    # There will be only two actions: launch or vertice.
    # If we choose a vertice, it will add the vertice to the state and update the new load weight, adding the vertice weight, and cost,
    # adding the weight * launch var cost.
    # If we choose a launch, it will add the new launch to the state and update the load weight to 0 and cost to the launch fixed cost.
    def transitionModel(self, state):
        successors = []
        actions = self.chooseActions(state)
        vertices = state[0]
        launches = state[1]
        for action in actions:
            loadWeight = state[2]
            newState = copy.deepcopy(state)
            if self.actionIsVertice(action):
                newState, loadWeight, g = self.addVertice(action, newState, loadWeight)
            elif self.actionIsLaunch(action):
                newState, loadWeight, g = self.addLaunch(action, newState, loadWeight)
            newState[2] = loadWeight
            h = self.heuristic(newState)
            """self.debugTransitionModel(state, action, newState, cost)"""
            successors.append({'state': newState, 'action': action, 'g': g, 'h': h})
        return successors

    # Checks if the action is choose a vertice.
    def actionIsVertice(self, action):
        if action[0] == 'V':
            return True
        return False

    # Checks if the action is choose a launch.
    def actionIsLaunch(self, action):
        if action[0] == 'L':
            return True
        return False

    # Adds the vertice to the state and updates the loadWeight, adding the weight of the vertice. The cost will be incremented too,
    # multiplying the vertice weight by the launch variable cost
    def addVertice(self, action, state, loadWeight):
        state[0].extend([action])
        loadWeight += self.verticesDict[action][0]
        g = self.verticesDict[action][0] * self.launchesDict[state[1][-1]][4]
        return (state, loadWeight, g)

    # Adds the launch to the state and refresh the loadWeight(will be 0 because there is a new launch to be loaded)
    # and cost (fixed cost of the chosen launch)
    def addLaunch(self, action, state, loadWeight):
        state[1].extend([action])
        loadWeight = 0
        g = self.launchesDict[action][3]
        return (state, loadWeight, g)

    # Checks if the state of the node is a goal state.
    # Our goal state is having all the vertices in orbit.
    def goalState(self, node):
        if set(node['state'][0]) == self.goal:
            return True
        return False

    # Heuristic of the problem.
    # Our heuristic value will be the cost of loading all of the remaining vertices (the vertices that are not in orbit or being loaded yet)
    # to the current launch.
    # This is an admissible heuristic of the relaxed problem, which 'removes' the weight constrain of the problem.
    def heuristic(self, state):
        if self.strategy is 'informed':
            vertices2goal = set(self.verticesDict.keys()) - set(state[0])
            lastLaunch = state[1][-1]
            h = 0
            if vertices2goal:
                for vertice in vertices2goal:
                    h += self.verticesDict[vertice][0] * self.launchesDict[lastLaunch][4]
        elif self.strategy is 'uninformed':
            h = 0
        return h

    # Checks if the nodes have the same state.
    # If they have the same vertices and launches.
    def equalState(self, node1, node2):
        if set(node1['state'][1]) == set(node2['state'][1]) and set(node1['state'][0]) == set(node2['state'][0]):
            return True
        return False

    # Write solution for terminal and in a file.
    def writeSolution(self, file, iteration, frontierSize, generatedNodes, start, solution):
        # Writing parameters to the file and terminal
        file.write(self.commands[2] + "\t" + self.strategy + "\n")
        print('\n\n\nITERATIONS\t', iteration)
        print('FRONTIER SIZE\t', frontierSize)
        print('GENERATED NODES\t', generatedNodes)
        print('EXECUTION TIME\t', time.time()-start)
        file.write("iterations\t" + str(iteration) + "\n")
        file.write("frontier size\t" + str(frontierSize) + "\n")
        file.write("generated nodes\t" + str(generatedNodes) + "\n")
        file.write("execution time\t" + str(time.time()-start) + "\n")

        # Solution print for file and terminal
        if solution:
            file.write("solution\n")
            print("\n\nSOLUTION")
            cost = 0
            for eachStep in solution[0]:
                if 'L' in eachStep:
                    if cost:
                        print(cost)
                        file.write(str(cost) + "\n")
                    print(self.launchesDict[eachStep][1], end=' ')
                    file.write(str(self.launchesDict[eachStep][1]) + "\t")
                    cost = self.launchesDict[eachStep][3]
                    varCost = self.launchesDict[eachStep][4]
                elif 'V' in eachStep:
                    print(eachStep, end=' ')
                    file.write(str(eachStep) + "\t")
                    cost += varCost*self.verticesDict[eachStep][0]
            print(cost, end='')
            file.write(str(cost) + "\n")
            print()
            print(solution[1])
            file.write(str(solution[1]) + "\n\n")
        else:
            print("\n\nNO SOLUTION\n", 0)
            file.write("no solution\n" + str(0)+"\n\n")

    # Shows the data processed from the read file.
    def debugData(self):
        print('\n=================================== LAUNCHES AVAILABLE')
        for key in [x[0] for x in sorted(self.launchesDict.items(), key=itemgetter(1))]:
            print('%s \t %s %s %s %s %s %s'
            % (key, self.launchesDict[key][0], self.launchesDict[key][1], self.launchesDict[key][2], self.launchesDict[key][3], self.launchesDict[key][4], self.launchesDict[key][5]))
        print('\n=================================== MODULES')
        for key in self.verticesDict.keys():
            print('%s \t %s' % (key, self.verticesDict[key][0]))
        print('\n=================================== CONNECTIONS')
        for key in self.verticesMapping.keys():
            print('%s \t %s' % (key, ' '.join(self.verticesMapping[key])))

    # Shows the state, the action that will be performed, the resulted state and action cost
    def debugTransitionModel(self, state, action, newState, cost):
        print('\nSTATE: ', state)
        print('ACTION: ', action)
        print('RESULTED STATE: ', newState)
        print('COST: ', cost)
