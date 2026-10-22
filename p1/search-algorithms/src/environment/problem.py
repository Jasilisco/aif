from src.environment.state import State
from src.environment.constants import MOVES

class Problem:
    """
    Implements the basic operations shared by all the search algorithms:
    available actions, state transitions, action cost and goal test.
    """

    def __init__(self, cfg):
        """
        Stores the configuration and creates the initial state.

        Args:
            cfg (Config): Configuration with the map, start and goal of the problem.
        """
        self.cfg = cfg
        self.initial = State(cfg.start[0], cfg.start[1], cfg.startOrientation)


    def can_move(self, s: State):
        """
        Checks whether the robot can advance in the direction it is facing.

        Args:
            s (State): Current state.

        Returns:
            bool: True if the destination cell is inside the map and is not an 
            impassable rock (value 0), False otherwise.
        """
        dx, dy = MOVES[s.o]
        nx, ny = s.x + dx, s.y + dy
        rows, cols = self.cfg.matrixSize
        return (0 <= nx < rows and 0 <= ny < cols and self.cfg.map[nx][ny] != 0)


    def actions(self, s: State):
        """
        Returns the actions that can be applied in a state.
        It is always allowed to rotate in any direction

        Args:
            s (State): Current state.

        Returns:
            list[str]: "Move" (only if allowed), "Rotate CW" and "Rotate CCW".
        """
        acts = ["Rotate CW", "Rotate CCW"]
        if self.can_move(s):
            acts.insert(0, "Move")
        return acts


    def result(self, s: State, action: str):
        """
        Returns the new state obtained after applying an action.

        Args:
            s (State): Current state.
            action (str): Action to apply: "Move", "Rotate CW" or "Rotate CCW".

        Returns:
            State: The new state.

        Raises:
            ValueError: If the action is unknown.
        """
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


    def cost(self, s: State, action: str):
        """
        Returns the cost of applying an action in a state.

        Args:
            s (State): State in which the action is applied.
            action (str): Action to apply: "Move", "Rotate CW" or "Rotate CCW".

        Returns:
            int: Hardness of the destination cell for "Move", 1 for any rotation.
        """
        cost = 1

        # If a move is allowed, the cost is the value of the cell to move in the map
        if action == "Move":
            dx, dy = MOVES[s.o]
            cost = int(self.cfg.map[s.x + dx][s.y + dy])
        return cost


    def is_goal(self, s: State):
        """
        Checks whether a state satisfies the goal.

        Args:
            s (State): State to check.

        Returns:
            bool: True if the position matches the goal and the orientation
                matches too or is irrelevant (8), False otherwise.
        """
        if (s.x, s.y) != self.cfg.goal:
            return False
        return self.cfg.goalOrientation == 8 or s.o == self.cfg.goalOrientation