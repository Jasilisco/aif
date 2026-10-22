from src.environment.state import State

class Node:
    """
    Node of the search tree: a state together with the information of how it was reached.
    """

    def __init__(self, state: State, g: int = 0, depth: int = 0, operator: str | None = None, parent: "Node | None" = None, h: int = 0):
        """
        Creates a node of the search tree.

        Args:
            state (State): State represented by the node.
            g (int, optional): Accumulated cost from the initial node.
            depth (int, optional): Depth of the node in the search tree.
            operator (str | None, optional): Action applied to the parent to reach this node. Defaults to None.
            parent (Node | None, optional): Parent node, None for the initial node. Defaults to None.
            h (int | None, optional): Heuristic value h(n), only meaningful for A*.
        """
        self.state = state
        self.g = g
        self.depth = depth
        self.operator = operator
        self.parent = parent
        self.h = h