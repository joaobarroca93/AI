from logic import Resolution
import operator
import copy
import time

class Search:
    def bfs(problem):
        ti = time.clock()
        frontier = []
        exploredSet = []
        node = Node(state = problem.initialState)
        frontier.append(node)
        # checks the max clause lenght of the clauses
        maxLen = 0
        for s in problem.possibleActions:
            if len(s) > maxLen: maxLen = len(s)
        if node.len > maxLen: maxLen = node.len
        # search loop
        while True:
            if not frontier or node.len > maxLen:
                # print("STOPPED AT Iter: {} | LastNodeLen: {} |  LastNodeDepth: {} | Time: {}s".format(len(exploredSet), node.len, node.depth, round(time.clock()-ti,3)))
                return False
            frontier.sort(key = operator.attrgetter('len'))
            node = frontier.pop(0)
            # print("Frontier: {} | Iter: {} | NodeLen: {} | NodeDepth: {}".format(len(frontier), len(exploredSet), node.len, node.depth))
            exploredSet.append(node)
            childNodes = node.expand(problem)
            for child in childNodes:
                if child.state == problem.goalState:
                    # print("STOPPED AT Iter: {} | LastNodeLen: {} |  LastNodeDepth: {} | Time: {}s".format(len(exploredSet), node.len, node.depth, round(time.clock()-ti,3)))
                    return True
                if not child.alreadyExplored(exploredSet) and not child.inFrontier(frontier):
                    frontier.append(child)

class Node:
    def __init__(self, state = [], parent = None, action = None, depth = 0, cost = 0):
        self.state = state
        self.action = action
        self.parent = parent
        self.depth = depth
        self.len = len(state)

    def __eq__(self, other):
        return set(self.state) == set(other.state)

    def expand(self, problem):
        actions = problem.actions(self.state)
        childNodes = []
        for action in actions:
            state = problem.result(copy.deepcopy(self.state), action)
            parent = self
            depth = self.depth + 1
            childNodes.append(Node(state, parent, action, depth))
        return childNodes

    def alreadyExplored(self, exploredSet):
        for node in exploredSet:
            if node == self:
                return True
        return False

    def inFrontier(self, frontier):
        for node in frontier:
            if node == self:
                return True
        return False

class StateSpace:
    def __init__(self, initialState, possibleActions):
        self.initialState = list()
        if isinstance(initialState, list) or isinstance(initialState, str):
            self.initialState.extend(initialState)
        else:
            self.initialState.append(initialState)
        self.possibleActions = possibleActions

    def actions(self, state):
        return self.possibleActions

    def transitionModel(self, state, action):
        if action:
            newState = Resolution.applyStep(state, action)
        return newState

class Problem(StateSpace):
    def __init__(self, initialState, possibleActions, goalState):
        super(Problem, self).__init__(initialState, possibleActions)
        self.goalState = goalState

    def result(self, state, action):
        return self.transitionModel(state, action)
