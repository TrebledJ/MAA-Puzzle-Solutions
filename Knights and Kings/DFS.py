from Node import Node
import Setup
from State import State


class DFS:
    """
    A class which performs a depth-first search.
    """
    def __init__(self):
        self.nodes_traversed = 0
        self.root = Node()

    def search(self):
        node = self.dfs(self.root)

        print('\n')
        if node is None:
            print('No Solution Found')
        else:
            print('Found Solution Node!')
            print('Nodes Traversed:', self.nodes_traversed)
            node.show()

        return node

    def dfs(self, node: Node):
        """
        Recursively searches for the solution node.
        First selects a next variable to assign to, then iterates through domain values.

        :param node: the current node
        :return: the solution node, None if not found
        """

        self.nodes_traversed += 1
        print('\nDFS at Node:', node.state.variable)

        next_variable = node.select_next_variable()
        print('> next variable:', next_variable)

        if next_variable is None:
            return None

        for value in Setup.domain_values:
            print(f'> ({next_variable}) checking assignment {next_variable} = {value}')
            if Setup.check_assignment(node.state.assignment, next_variable, value):
                print(f'Assigning variable {next_variable} with {value} (depth={node.depth})')
                state = State(node.state.assignment, next_variable, value)
                new_node = Node(state, node.depth)
                if new_node.is_solution():
                    return new_node

                result_node = self.dfs(new_node)
                if result_node is not None and result_node.is_solution():
                    return result_node
            else:
                print('> ! skipping', next_variable, '=', value)

        print('  < backtracking')
        return None
