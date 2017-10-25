# Artificial Inteligence
@author: João Barroca <joao.barroca@tecnico.ulisboa.pt>

IN ORBIT ASSEMBLY OF LARGE STRUCTURES

This program aims to solve the problem of scheduling the launch of components for the in orbit assembly of a large structure. Given a set of components to be launched, a launch timeline and costs, and a construction plan, the goal is to determine the assignment of components to launches, such as the total cost is minimized.

First, we define the problem (PROBLEM FORMUTALION) and the we use uninformed (UNIFORM-COST SEARCH) and informed (A*) search methods to find the solution.

To test the solution, use the command:
python solver.py -i(informed)/-u(uninformed) textfile.txt
