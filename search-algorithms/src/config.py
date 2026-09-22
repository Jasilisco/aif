import sys
import os
import utils as ut
import numpy as np

class Config:
    
    orientations = {
        0: 'North',
        1: 'Northeast',
        2: 'East',
        3: 'Southeast',
        4: 'South',
        5: 'Southwest',
        6: 'West',
        7: 'Northwest',
        8: 'Irrelevant'
    }
    
    def __init__(self, filePath):
        path = f"../input/{filePath}.txt"
        self.filePath = path
        if not os.path.exists(self.filePath):
            raise FileNotFoundError(f"Input file not found: {self.filePath}")
        self._load(self.filePath)
        self.declare_content()
    
    def declare_content(self): 
        print('--- SEARCH ALGORITHMS ENVIRONMENT ---')
        print(f'#1 - Board size: {self.matrixSize}')
        print('#2 - Board layout: ')
        print('')
        print('\n'.join(' '.join(str(int(item)) for item in line) for line in self.board))
        print('')
        print(f'#3 - Starting position {self.start}, starting orientation {self.orientations[self.startOrientation]}')
        print(f'#4 - Goal position {self.goal}, goal orientation {self.orientations[self.goalOrientation]}')
        print('------------------------------')
        print("\n")
        
    def start_state(self):
        return (self.start[0], self.start[1], self.startOrientation)
    
    def goal_state(self):
        return (self.goal[0], self.goal[1], self.goalOrientation)
    
    def _load(self, filePath):
        with open(filePath, 'r') as file:
            content = file.readlines()
            self.matrixSize = tuple(map(int, content[0].split()))
            self.board = self._board(content[1:self.matrixSize[0] + 1])
            self.start, self.goal, self.startOrientation, self.goalOrientation = self._path(content[self.matrixSize[0] + 1:])
            
    def _board(self, board):
        boardAux = []
        for line in board:
            boardAux.append(line.split())
        return np.array(boardAux,dtype=float)
    
    def _path(self, path):
        start = tuple(map(int, path[0].split()[:2]))
        goal = tuple(map(int, path[1].split()[:2]))
        startOrientation = int(path[0].split()[2])
        goalOrientation = int(path[1].split()[2])
        return start, goal, startOrientation, goalOrientation