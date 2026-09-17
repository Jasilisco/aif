# AI FUNDAMENTALS P1 - Search Algorithms

First Practice about applying search algorithms to solve shortest path/optimal path problem

## Folder Structure

```
search-algorithms/
├── input/                    # Folder to place input text files
├── src/                      # Source Code 
│   ├── config.py                   # Config Class - Organizes and declares the input
│   ├── main.py                     # Main file to start the execution
│   └── utils.py                    # Contains util functions
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
cd .\src\
python3 .\main.py input_file
```

Note: The name of the input file must be without extension