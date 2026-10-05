# AI FUNDAMENTALS P1 - Search Algorithms

First Practice about applying search algorithms to solve shortest path/optimal path problem

## Folder Structure

```
search-algorithms/
├── input/                    # Folder to place input text files
├── src/                      # Source Code 
│   ├── environment/                # Contains the classes that structures the problem
│   │   ├── config.py                   # Config Class - Organizes and declares the input
│   │   ├── constants.py                # Constants File - Constant dictionaries
│   │   ├── problem.py                  # Problem Class - Includes shared functions to solve the problems
│   │   └── state.py                    # State Class - Declares a inmutable state of a node
│   ├── search-problem/             # Contains the classes that solve the problem
│   │   ├── algorithms/                 # Contains the classes that implement the algorithms
│   │   └── search.py                   # Search Class - Base class for the algorithms to implement
├── main.py                     # Main file to start the execution
└── requirements.txt          # Contains the libraries required for the execution
```

## Steps to execute

# 1.- Clone Repository

Either by GitDesktop or by GitBash

# 2.- Build and activate Virtual Environment (Windows version)

```sh
cd .\search-algorithms\
python3 -m venv aif
.\aif\Scripts\activate
```

# 3.- Install requirements

```sh
python3 -m pip install -r requirements.txt
```

# 4.- Place Input Files

Must follow the specified format for input which is the following

```
Matrix Size
Matrix Board
Start Coordinates & orientation
Goal Coordinates & orientation
```

The character separators must be spaces and the characters must be numbers. Example below for matrix size = (3,3), matrix board = [[3 2 4],[2 3 1],[1 4 2]], start coordinates = (0,0) and orientation = 0 (North), goal coordinates = (2,2) and orientation = 8 (Irrelevant):

```
3 3
3 2 4
2 3 1
1 4 2
0 0 0
2 2 8
```

# 5.- Execution

```sh
python3 .\main.py input_file
```

Note: The name of the input file must be without extension