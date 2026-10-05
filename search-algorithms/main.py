from src.environment.config import Config
import sys
import warnings
from src.environment.problem import Problem
from src.search.algorithms.astar import Astar

def main():
    pass

if __name__ == "__main__":
    if len(sys.argv) < 2:
        raise ValueError("The name of the input file must be provided")
    cfg = Config(sys.argv[1])
    cfg.declare_content()
    if len(sys.argv) >= 3 and sys.argv[2] == '-a':
        match sys.argv[3]:
            case 'astar':
                if(len(sys.argv) >= 5 and sys.argv[4] == '-h'):
                    match sys.argv[5]:
                        case 'manhattan':
                            astar = Astar(Problem(cfg), 'manhattan')
                        case 'chessboard':
                            astar = Astar(Problem(cfg))
                        case _:
                            astar = Astar(Problem(cfg))
                            warnings.warn("Heuristic not recognized or not implemented. Using Chessboard heuristic", UserWarning)
                    astar.solve_astar()
            case _:
               raise ValueError("The algorithm is not recognized") 
    else:
        raise ValueError("The flag is not recognized or algorithm not specified")
    
    