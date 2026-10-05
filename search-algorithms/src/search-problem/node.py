from state import State

class Node:
    def __init__(self, state: State, g: int = 0, depth: int = 0, operator: str | None = None, parent: "Node | None" = None, h: int = 0):
        self.state = state
        self.g = g
        self.depth = depth
        self.operator = operator
        self.parent = parent
        self.h = h
