from collections import namedtuple
import copy
import numpy as np

# instantiate a Point type
Point = namedtuple('Point', ['x', 'y'])


class Grid:
    """
    Constructs and stores a grid object, with convenience indexing.

    Example:
        grid = Grid(np.array([[ 0, 1, 2 ],
                              [ 3, 4, 5 ],
                              [ 6, 7, 8 ]]))
        print(grid[1, 1]) = 4


    """
    def __init__(self, grid: np.ndarray):
        self.grid = copy.deepcopy(grid)

    def __getitem__(self, key):
        if isinstance(key, Point):
            return self.grid[key.y, key.x]

        return self.grid.__getitem__(key)

    def __setitem__(self, key, value):
        if isinstance(key, Point):
            self.grid[key.y, key.x] = value

        return self.grid.__setitem__(key, value)

    def __len__(self): return len(self.grid)
    def __str__(self): return str(self.grid)
