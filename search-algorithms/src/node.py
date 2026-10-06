class Node:
    def __init__(self, state, g, depth, operator, parent=None):
        self.state = state
        self.g = g
        self.depth = depth
        self.operator = operator
        self.parent = parent
        self.children = []


    def set_child(self, child):
        """
        Adds a child node to the node.

        Args:
            child: Node object representing the child.
        """
        child.parent = self
        self.children.append(child)