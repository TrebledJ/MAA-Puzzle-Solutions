from collections import OrderedDict
import copy


class State:
    """
    A STATE represents an assigned instance of the grid.
    """

    def __init__(self, assignment=None, variable=None, value=None):
        """
        Performs an assignment, creating a new assignment on construction.
        :param assignment: dict
        :param variable: Point
        :param value: str
        """

        if assignment is None:
            self.assignment = OrderedDict()
        else:
            self.assignment = copy.deepcopy(assignment)

        if variable is not None:
            self.assignment[variable] = value

        self.variable = variable
