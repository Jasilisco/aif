from dataclasses import dataclass

@dataclass(frozen=True)
class State:
    """
    Represents a state of the robot: its position on the map and its orientation.

    Attributes:
        x (int): Row of the robot on the map.
        y (int): Column of the robot on the map.
        o (int): Orientation, from 0 (North) to 7 (Northwest), clockwise.
    """
    x: int
    y: int
    o: int                       

    def __str__(self):
        """
        Returns the state as text, in the format (x,y,o).

        Returns:
            str: Text representation of the state.
        """
        return f"({self.x},{self.y},{self.o})"