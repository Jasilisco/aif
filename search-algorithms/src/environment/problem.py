from src.environment.state import State
from src.environment.constants import MOVES

# Class that implements the basic operations to perform shared by all algorithms
# Recovers the basic configuration and allows operations like cost calculation, goal calculation or movement calculation
class Problem:
    def __init__(self, cfg):
        self.cfg = cfg
        self.initial = State(cfg.start[0], cfg.start[1], cfg.startOrientation)

    # Returns True or false whether the movement is allowed or not
    # Movement is ONLY allowed in the direction to which the robot is facing, so is only needed to check that direction
    def can_move(self, s: State):
        dx, dy = MOVES[s.o]
        nx, ny = s.x + dx, s.y + dy
        rows, cols = self.cfg.matrixSize
        return (0 <= nx < rows and 0 <= ny < cols and self.cfg.board[nx][ny] != 0)

    # Returns all possible actions given a state
    def actions(self, s: State):
        # Its always allowed to rotate in any direction
        acts = ["Rotate CW", "Rotate CCW"]
        # Check whether movement is allowed or not
        if self.can_move(s):
            acts.insert(0, "Move")
        return acts

    # Returns the new state given the past state and the action applied
    def result(self, s: State, action: str):
        # If the robot decides to move, the new state is the application of the movement to the past state
        if action == "Move":
            dx, dy = MOVES[s.o]
            return State(s.x + dx, s.y + dy, s.o)
        # If the robot decides to rotate, the new state is adding or substrating 1 to the current rotation
        if action == "Rotate CW":
            return State(s.x, s.y, (s.o + 1) % 8)
        if action == "Rotate CCW":
            return State(s.x, s.y, (s.o - 1) % 8)
        raise ValueError(f"Unknown action: {action}")

    # Returns the cost of an action given a state
    def cost(self, s: State, action: str):
        # Base cost for orientation change
        cost = 1
        # If a move is allowed, the cost is the value of the cell to move in the board
        if action == "Move":
            dx, dy = MOVES[s.o]
            cost = int(self.cfg.board[s.x + dx][s.y + dy])
        return cost

    # Returns True if the given state is the goal of the problem
    def is_goal(self, s: State):
        # The goal is reached if the current state matches the goal coordinates and the orientation is the same or irrelevant
        if (s.x, s.y) != self.cfg.goal:
            return False
        return self.cfg.goalOrientation == 8 or s.o == self.cfg.goalOrientation