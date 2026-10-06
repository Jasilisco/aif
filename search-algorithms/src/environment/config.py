import numpy as np
from src.environment.constants import ORIENTATIONS
from pathlib import Path


# Class that receives a text file and extracts and stores all the constant information of the problem from that file, such as goal, start, orientations and board
class Config:
    INPUT_DIR = Path(__file__).resolve().parents[2] / "input"
    
    # Checks the path for the file and opens it
    def __init__(self, filePath):
        self.filePath = self.INPUT_DIR / f"{filePath}.txt"
        if not self.filePath.exists():
            raise FileNotFoundError(f"Input file not found: {self.filePath}")
        self._load(self.filePath)
    
    # Method to declare all the content of the problem
    def declare_content(self): 
        print('--- SEARCH ALGORITHMS ENVIRONMENT ---')
        print(f'#1 - Board size: {self.matrixSize}')
        print('#2 - Board layout: ')
        print('')
        print('\n'.join(' '.join(map(str, line)) for line in self.board))
        print('')
        print(f'#3 - Starting position {self.start}, starting orientation {ORIENTATIONS[self.startOrientation]}')
        print(f'#4 - Goal position {self.goal}, goal orientation {ORIENTATIONS[self.goalOrientation]} \n')
    
    # Extracts and stores the board, orientation and positions
    def _load(self, filePath):
        with open(filePath, 'r') as file:
            content = file.readlines()
            self.matrixSize = tuple(map(int, content[0].split()))
            self.board = self._board(content[1:self.matrixSize[0] + 1])
            self.start, self.goal, self.startOrientation, self.goalOrientation = self._path(content[self.matrixSize[0] + 1:])
    
    # Reads the board and returns it as an int matrix     
    def _board(self, board):
        boardAux = []
        for line in board:
            boardAux.append(line.split())
        return np.array(boardAux,dtype=int)
    
    # Reads the orientation and the position and returns it as tuples and integers
    def _path(self, path):
        start = tuple(map(int, path[0].split()[:2]))
        goal = tuple(map(int, path[1].split()[:2]))
        startOrientation = int(path[0].split()[2])
        goalOrientation = int(path[1].split()[2])
        return start, goal, startOrientation, goalOrientation
    