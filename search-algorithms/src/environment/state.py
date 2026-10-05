from dataclasses import dataclass

@dataclass(frozen=True)
class State:
    x: int
    y: int
    o: int                       

    def __str__(self):
        return f"({self.x},{self.y},{self.o})"