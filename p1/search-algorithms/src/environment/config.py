import numpy as np
from src.environment.constants import ORIENTATIONS
from pathlib import Path

INPUT_DIR = Path(__file__).resolve().parents[2] / "input"

class Config:
    """
    Reads a map text file and stores the constant information of the problem:
    map, start and goal positions, and their orientations.
    """
    
    def __init__(self, filePath):
        """
        Checks that the map file exists and loads its content.

        Args:
            filePath (str): Name of the map file in the input folder.

        Raises:
            FileNotFoundError: If the file does not exist in the input folder.
        """
        self.filePath = INPUT_DIR / f"{filePath}.txt"
        if not self.filePath.exists():
            raise FileNotFoundError(f"Input file not found: {self.filePath}")
        self.load(self.filePath)


    def declare_content(self):
        """
        Prints all the content of the problem: map size, map layout, start and goal.
        """
        print('')
        print('--- SEARCH ALGORITHMS ENVIRONMENT ---')
        print('')
        print(f'#1 - Map size: {self.matrixSize}')
        print('#2 - Map layout: ')
        print('')
        print('\n'.join(' '.join(map(str, line)) for line in self.map))
        print('')
        print(f'#3 - Starting position {self.start}, starting orientation {ORIENTATIONS[self.startOrientation]}')
        print(f'#4 - Goal position {self.goal}, goal orientation {ORIENTATIONS[self.goalOrientation]}')
        print('')


    def load(self, filePath):
        """
        Extracts and stores the map size, map, positions and orientations from the file.

        Args:
            filePath (Path): Path of the map file.
        """
        with open(filePath, 'r') as file:
            content = file.readlines()
            self.matrixSize = tuple(map(int, content[0].split()))
            self.map = self.load_map(content[1:self.matrixSize[0] + 1])
            self.start, self.goal, self.startOrientation, self.goalOrientation = self.load_path(content[self.matrixSize[0] + 1:])


    def load_map(self, map):
        """
        Reads the map lines and converts them into an integer matrix.

        Args:
            map (list[str]): Lines of the file that contain the map.

        Returns:
            np.ndarray: Matrix of ints with the hardness of each cell.
        """
        mapAux = []
        for line in map:
            mapAux.append(line.split())
        return np.array(mapAux,dtype=int)


    def load_path(self, path):
        """
        Reads the start and goal lines and extracts positions and orientations.

        Args:
            path (list[str]): The last two lines of the file (start and goal), each as "x y o".

        Returns:
            tuple: (start, goal, startOrientation, goalOrientation), where start and goal
                are (x, y) tuples and the orientations are ints.
        """
        start = tuple(map(int, path[0].split()[:2]))
        goal = tuple(map(int, path[1].split()[:2]))
        startOrientation = int(path[0].split()[2])
        goalOrientation = int(path[1].split()[2])
        return start, goal, startOrientation, goalOrientation