from src.environment.config import Config
import sys
import warnings
from src.environment.problem import Problem
from src.search.algorithms.astar import Astar
from src.search.algorithms.sbf import bfs
from src.search.algorithms.sdf import dfs
from src.environment.utils import print_trace

def main():
    pass

if __name__ == "__main__":
    if len(sys.argv) < 2:
        raise ValueError("The name of the input file must be provided")
    cfg = Config(sys.argv[1])
    cfg.declare_content()
    if len(sys.argv) >= 3 and sys.argv[2] == '-a':
        print('--- SOLVING PROBLEM ---')
        match sys.argv[3]:
            case 'bfs':
                print('Algorithm: Breadth First')
                solution, last, n_exp, n_front = bfs(Problem(cfg))
                print_trace(solution, last, n_exp, n_front)
                pass
            case 'dfs':
                print('Algorithm: Depth First')
                solution, last, n_exp, n_front = dfs(Problem(cfg))
                print_trace(solution, last, n_exp, n_front)
                pass
            case 'astar':
                if(len(sys.argv) >= 5 and sys.argv[4] == '-h'):
                    print('Algorithm: A*')   
                    match sys.argv[5]:
                        case 'manhattan':
                            print('Heuristic: Weighted Manhattan Distance')
                            astar = Astar(Problem(cfg), 'manhattan')
                        case 'chessboard':
                            print('Heuristic: Weighted Chessboard Distance')
                            astar = Astar(Problem(cfg))
                        case _:
                            astar = Astar(Problem(cfg))
                            warnings.warn("Heuristic not recognized or not implemented. Using Chessboard heuristic", UserWarning)
                            print('Heuristic: Weighted Chessboard Distance')
                else:
                    print('Heuristic: Weighted Chessboard Distance')
                    astar = Astar(Problem(cfg))
                astar.solve_astar()
            case _:
               raise ValueError("The algorithm is not recognized") 
    else:
        raise ValueError("The flag is not recognized or algorithm not specified")
    
    