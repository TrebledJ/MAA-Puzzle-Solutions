import numpy as np

from DFS import DFS
from Grid import Grid
import Setup

"""

Puzzle from MAA Focus Volume 39, No. 1, February/March 2019

============================

Knights and Kings
– David Nacin

Fill in the cells with knights and kings so that every row and column
contains the same number of each. The numeric clues indicate the
number of pieces of the same type that the piece in the cell can attack.

For example, a clue of 4 in a cell indicates that there is either a knight in
that cell that can attack four other knights, or a king in that cell that can
attack four other knights. #

============================

Sample solved 4 by 4 puzzle

H = Horse
K = King

    0    2    3    2
  H    H    K    K
    2    4    4    2
  H    K    K    H
    3    4    2    1
  K    K    H    H
    2    2    1    0
  K    H    H    K

============================

Attempt to model the Knights and Kings puzzle as a Constraint Satisfaction Problem (CSP)

"""


"""
Let n be the width of the grid. Assume the grid to have equal width and height.  

Ordinary brute force yields 2^(n*n) possibilities and nodes to check.

Brute force yields:

grid_a: 2^(4*4) = 65536 nodes
grid_b: 2^(6*6) = 68719476736 nodes ~ 6.87 x 10^10
grid_c: 2^(8*8) ~ 1.84 x 10^19 

A first attempt with depth-first search and yielded:

grid_a: 159/34 nodes        (over 0.0025/0.00052% [2.5 x 10^-3 / 5.2 x 10^-4 %] saved)
grid_b: 81/95 nodes        (over 0.000000019/0.0000000014% [1.9 x 10^-8 / 1.4 x 10^-9 %] saved) 
grid_c: 4798/4356 nodes      (over 2.7 x 10^-16 / 2.4 x 10^-16 % saved)

N.B. a/b corresponds to the number of nodes where the setup in <a> has

    domain_values = ['knight', 'king']
    
and the setup in <b> has

    domain_values = ['king', 'knight']. 



"""

print("Grid:\n", Setup.grid)
print(f"(Size {Setup.grid_size})")

dfs = DFS()
node = dfs.search()

grid = Grid(np.ndarray((Setup.grid_size, Setup.grid_size), dtype=str))
for point, value in node.state.assignment.items():
    grid[point] = ['O', 'K'][value == 'knight']

print("Grid:\n", grid)







