import copy
import itertools
import numpy as np

from Grid import Grid, Point
import Grids

"""
Possible Grids:
grid_king_ex
grid_knight_ex
grid_ex
grid_a
grid_b
grid_c
"""

grid = Grid(np.array(Grids.grid_ex))
grid_size = len(grid)

# coordinates on the grid
variables = [Point(i, j) for i, j in itertools.product(range(grid_size), range(grid_size))]

# identify domain (the possible values each variable can take)
domain_values = ['knight', 'king']


def get_attack_points(point: Point, value: str):
    """
    :param point: Point
    :param value: str
    :return: a list of points which can be attacked by a <value> piece on <point>
    """
    if value == 'knight':
        # check and count all possible knight attack positions
        #   generate (-1, -2), (+1, -2), (-1, +2), ... mappings
        mappings = list(itertools.product([-1, 1], [-2, 2])) + list(itertools.product([-2, 2], [-1, 1]))
    elif value == 'king':
        # check and count all possible king attack positions
        mappings = list(itertools.product([-1, 0, 1], [-1, 0, 1]))
        mappings.remove((0, 0))
    else:
        raise ValueError(f'Value {value} not recognised.')

    ret = [Point(point.x + dx, point.y + dy) for dx, dy in mappings
           if 0 <= point.x + dx < grid_size and 0 <= point.y + dy < grid_size]

    return ret


attack_points_knight = Grid(np.array(
    [[get_attack_points(Point(i, j), 'knight') for i in range(grid_size)] for j in range(grid_size)]
))

attack_points_king = Grid(np.array(
    [[get_attack_points(Point(i, j), 'king') for i in range(grid_size)] for j in range(grid_size)]
))


def check_constraint_satisfied(assignments: dict, variable: Point, value: str):
    attack_points = attack_points_knight[variable] if value == 'knight' else attack_points_king[variable]

    if len(attack_points) < grid[variable]:
        print(f'    > insufficient attack points for {value} at {variable} ({len(attack_points)}, required {grid[variable]})')
        return False

    count_attackable_knights = sum(1 for p in attack_points if p in assignments and assignments[p] == 'knight')
    count_attackable_kings = sum(1 for p in attack_points if p in assignments and assignments[p] == 'king')
    free_spaces = len(attack_points) - count_attackable_kings - count_attackable_knights

    if value == 'knight':
        if count_attackable_knights > grid[variable]:
            print(f'    > too many attackable knights at {variable} ({count_attackable_knights}, required {grid[variable]})')
            return False
        if free_spaces + count_attackable_knights < grid[variable]:
            print(f'    > insufficient attackable knights (and free spaces) for {variable} (free {free_spaces}, attackable {count_attackable_knights}, required {grid[variable]})')
            return False

    if value == 'king':
        if count_attackable_kings > grid[variable]:
            print(f'    > too many attackable kings at {variable} ({count_attackable_kings}, required {grid[variable]})')
            return False
        if free_spaces + count_attackable_kings < grid[variable]:
            print(f'    > insufficient attackable kings (and free spaces) for {variable} (free {free_spaces}, attackable {count_attackable_kings}, required {grid[variable]})')
            return False

    # check if all attack points are occupied
    if all(p in assignments for p in attack_points):
        # check whether knights constraint is satisfied
        if value == 'knight' and grid[variable] != count_attackable_knights:
            print(f'    > mismatch of attackable knights at {variable} (attackable {count_attackable_knights}, required {grid[variable]})')
            return False

        if value == 'king' and grid[variable] != count_attackable_kings:
            print(f'    > mismatch attackable kings at {variable} (attackable {count_attackable_kings}, required {grid[variable]})')
            return False

    return True


def check_assignment(assignments: dict, point: Point, value: str) -> bool:
    """
    Checks whether assigning <variable> to <value> with the given <assignments> may satisfy the constraints.
    :param assignments: dict or OrderedDict with variable -> value pairs
    :param point: the variable to be assigned to
    :param value: the value to assign
    :return: True or False depending on whether an assignment is possible
    """

    # check base condition: do the constraints hold for current point
    if not check_constraint_satisfied(assignments, point, value):
        print('    → base constraint failed:', point, '=', value)
        return False

    # check neighbouring conditions: do the constraints (still) hold for other points
    temp_assignment = copy.deepcopy(assignments)
    temp_assignment[point] = value

    # loop through points that can attack the current point, as kings
    print('  > checking neighbouring kings')
    for pt in filter(lambda p: p in assignments and assignments[p] == 'king', attack_points_king[point]):
        if not check_constraint_satisfied(temp_assignment, pt, assignments[pt]):
            print('    → neighbouring constraint failed for neighbour', pt, '=', assignments[pt])
            return False

    # loop through points that can attack the current point, as knights
    print('  > checking neighbouring knights')
    for pt in filter(lambda p: p in assignments and assignments[p] == 'knight', attack_points_knight[point]):
        if not check_constraint_satisfied(temp_assignment, pt, assignments[pt]):
            print('    → neighbouring constraint failed for neighbour', pt, '=', assignments[pt])
            return False

    # all constraints are satisfied!
    return True
