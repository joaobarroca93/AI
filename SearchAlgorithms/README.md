# IN ORBIT ASSEMBLY OF LARGE STRUCTURES

This program aims to solve the problem of scheduling the launch of components for the in orbit assembly of a large structure. Given a set of components to be launched, a launch timeline and costs, and a construction plan, the goal is to determine the assignment of components to launches, such as the total cost is minimized.

The program reads a text file which contains vertices (corresponding to the modules of the space station and that contain the weight of the module), edges (which represent the connections between the modules) and launches (containing a date, a maximum payload, a fixed cost and a variable cost).

Then we formulate the problem defining the state space (which contain the initial state and the transition model between the states), the problem goal and the possible actions.

Finally we use an uninformed search algorithm (UNIFORM-COST SEARCH) and an informed search algorithm (A*) to find the optimal solution.

To test, use the command:
python solver.py -i(informed)/-u(uninformed) textfile.txt

The program will create a file named "AI.txt" that contains the solution and the time and number of iterations to solve the problem.





Copyright (C) {2017} {João Barroca}

This program is free software: you can redistribute it and/or modify it under the terms of the GNU General Public License as published by the Free Software Foundation, either version 3 of the License, or (at your option) any later version.

This program is distributed in the hope that it will be useful, but WITHOUT ANY WARRANTY; without even the implied warranty of MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE. See the GNU General Public License for more details.

You should have received a copy of the GNU General Public License along with this program. If not, see <http://www.gnu.org/licenses/>.

To contact, please use <joao.barroca@tecnico.ulisboa.pt>
