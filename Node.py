import numpy as np
import matplotlib.pyplot as plt

from Grid import Point
import Setup
from State import State


class Node:
    """
    A NODE holds a state and depth in a DFS tree. It is delegated the task of selecting a next variable,
    checking whether the solution has been reached, and drawing the state.
    """

    def __init__(self, state=None, depth=0):
        if state is None:
            self.state = State()
        else:
            self.state = state

        self.depth = depth+1

    def select_next_variable(self) -> Point:
        # TODO select variable by Most Constrained Domain, and tie-break by Most Domain-Constraining

        if self.state.variable is None:
            return Point(0, 0)

        if self.state.variable.x+1 == Setup.grid_size:
            if self.state.variable.y + 1 == Setup.grid_size:
                return None

            return Point(0, self.state.variable.y+1)

        return Point(self.state.variable.x+1, self.state.variable.y)

    def is_solution(self) -> bool:
        return len(self.state.assignment) == Setup.grid_size * Setup.grid_size

    def draw(self):
        image = np.zeros((Setup.grid_size, Setup.grid_size, 3), np.uint8)
        for variable in self.state.assignment:
            if self.state.assignment[variable] == 'knight':
                image[variable.y, variable.x] = [255, 255, 255]     # white mustang
                plt.text(variable.x-0.4, variable.y+0.4, 'Knight', fontsize=16)
            if self.state.assignment[variable] == 'king':
                image[variable.y, variable.x] = [255, 0, 0]         # royal red
                plt.text(variable.x-0.4, variable.y+0.4, 'King', fontsize=16)

        for point in Setup.variables:
            color = ['white', 'black'][point in self.state.assignment]
            plt.text(point.x + 0.2, point.y - 0.2, Setup.grid[point], fontsize=16, color=color)

        return image

    def show(self):
        plt.imshow(self.draw())
        plt.axis('off')
        plt.show()
