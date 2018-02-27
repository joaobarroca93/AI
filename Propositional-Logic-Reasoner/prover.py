import sys
from logic import Clause
from search import Problem, Search

def read_stdin():
    data = sys.stdin.readlines()
    sentences = []
    for i in range(len(data)):
        data[i] = data[i].replace('\n','')
    for s in data:
        if s: sentences.append(eval(s))
    return sentences

def main():
    rawClauses = read_stdin()
    clauseInst = Clause(rawClauses)

    resolution = Problem(initialState = [],
        possibleActions = clauseInst.clausesList, goalState = [])
        
    status = Search.bfs(resolution)
    print("\n{}".format(status))


if __name__ == '__main__':
    main()
