# Artificial Inteligence
@author: João Barroca <joao.barroca@tecnico.ulisboa.pt>

IN ORBIT ASSEMBLY OF LARGE STRUCTURES

This program aims to solve the problem of scheduling the launch of components for the in orbit assembly of a large structure. Given a set of components to be launched, a launch timeline and costs, and a construction plan, the goal is to determine the assignment of components to launches, such as the total cost is minimized.

The program reads a text file which contains vertices (corresponding to the modules of the space station and that contain the weight of the module), edges (which represent the connections between the modules) and launches (containing a date, a maximum payload, a fixed cost and a variable cost).

Then we formulate the problem defining the state space (which contain the initial state and the transition model between the states), the problem goal and the possible actions.

Finally we use an uninformed search algorithm (UNIFORM-COST SEARCH) and an informed search algorithm (A*) to find the optimal solution.

To test, use the command:
python solver.py -i(informed)/-u(uninformed) textfile.txt

The program will create a file named "AI.txt" that contains the solution and the time and number of iterations to solve the problem.
