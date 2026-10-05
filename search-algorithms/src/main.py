import sys
from config import Config
from sbf import bfs
from sdf import dfs
from utils import print_trace

def main():
    cfg = Config(sys.argv[1])
    #solution, last, n_exp, n_front = bfs(cfg.board, cfg.start_state(), cfg.goal_state())
    solution, last, n_exp, n_front = dfs(cfg.board, cfg.start_state(), cfg.goal_state())
    print_trace(solution, last, n_exp, n_front)

if __name__ == "__main__":
    main()