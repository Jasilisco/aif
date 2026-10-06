import numpy as np
from src.environment.constants import ORIENTATIONS
from pathlib import Path

INPUT_DIR = Path(__file__).resolve().parents[2] / "input"

# Class that receives a text file and extracts and stores all the constant information of the problem from that file, such as goal, start, orientations and map
class Config:
    
    # Checks the path for the file and opens it
    def __init__(self, filePath):
        self.filePath = INPUT_DIR / f"{filePath}.txt"
        if not self.filePath.exists():
            raise FileNotFoundError(f"Input file not found: {self.filePath}")
        self.load(self.filePath)
    
    # Method to declare all the content of the problem
    def declare_content(self): 
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
    
    # Extracts and stores the map, orientation and positions
    def load(self, filePath):
        with open(filePath, 'r') as file:
            content = file.readlines()
            self.matrixSize = tuple(map(int, content[0].split()))
            self.map = self.load_map(content[1:self.matrixSize[0] + 1])
            self.start, self.goal, self.startOrientation, self.goalOrientation = self.load_path(content[self.matrixSize[0] + 1:])
    
    # Reads the map and returns it as an int matrix     
    def load_map(self, map):
        mapAux = []
        for line in map:
            mapAux.append(line.split())
        return np.array(mapAux,dtype=int)
    
    # Reads the orientation and the position and returns it as tuples and integers
    def load_path(self, path):
        start = tuple(map(int, path[0].split()[:2]))
        goal = tuple(map(int, path[1].split()[:2]))
        startOrientation = int(path[0].split()[2])
        goalOrientation = int(path[1].split()[2])
        return start, goal, startOrientation, goalOrientation
    