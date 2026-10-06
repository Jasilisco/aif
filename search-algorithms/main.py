from src.environment.config import Config, INPUT_DIR
from src.environment.problem import Problem
from src.search.algorithms.astar import Astar
from src.search.algorithms.sbf import bfs
from src.search.algorithms.sdf import dfs
from src.environment.utils import print_trace
from src.environment.constants import ALGORITHM_NAMES, HEURISTIC_NAMES, SEED
from src.search.randomMapGenerator import PipelineGenerator
import numpy as np

def pick_setting(title, parse, default=None, prompt="> "):
    print(f"\n{title}")
    while True:
        answer = input(prompt).strip()
        if answer == "" and default is not None:
            return default
        try:
            return parse(answer)
        except ValueError as error:
            print(error)
     
def env_setting(title, options, default=None):
    keys = list(options)
    for i, key in enumerate(keys, start=1):
        title += f"\n  {i}. {options[key]}"
    def parse(answer):
        if answer.isdigit() and 1 <= int(answer) <= len(keys):
            return keys[int(answer) - 1]
        raise ValueError(f"Please enter a number between 1 and {len(keys)}.")
    return pick_setting(title, parse, default)

def pipeline_seed(default=SEED):
    def parse(answer):
        if answer.isdigit():
            return int(answer)
        raise ValueError("Please enter a numeric seed.")
    return pick_setting(f"Enter a numeric seed (default: {default}):", parse, default)

def input_file():
    available = sorted(p.stem for p in INPUT_DIR.glob("*.txt"))
    def parse(answer):
        if not answer:
            raise ValueError("File name cannot be empty.")
        if not (INPUT_DIR / f"{answer}.txt").exists():
            raise ValueError(f"File not found: {answer}.txt")
        return answer
    return pick_setting(f"Input file:\n  Available maps: {', '.join(available)}",
               parse, prompt="  Enter name: ")

def set_env():
    print("--- SEARCH ALGORITHMS AUTOMATED SOLVER ---")
    print('')
    print("To set the environment, pick a number between the following options (empty for default):")
    mode = env_setting("Execution mode (default: Map from the input folder):", {
        "single": "Solve a map from the input folder",
        "random": "Run a pipeline on random generated maps",
    }, "single")
    if mode == "random":
        return {"random": True, "map": None, "algorithm": None, "heuristic": None}
    filePath = input_file()
    algorithm = env_setting("Algorithm (default: A*):", ALGORITHM_NAMES, "astar")
    heuristic = None
    if algorithm == "astar":
        heuristic = env_setting("Heuristic (default: Weighted Chessboard Distance):", HEURISTIC_NAMES, "chessboard")
    return {"random": False, "map": filePath, "algorithm": algorithm, "heuristic": heuristic}

def random_pipeline():
    if(env_setting("Would you like to set a seed for reproducibility purposes or use a random one? (default: random seed)", {1: "Select a seed", 0: "Use a random seed"}, 0)):
        seed = pipeline_seed()
    else:
        seed = np.random.randint(0, 10000)
    print(f"Using Seed: {seed}")
    print('')
    print('20 random maps will be generated and solved using all the implemented algorithms')
    print('')
    heuristic = env_setting("Heuristic for A* (default: Weighted Chessboard Distance):", HEURISTIC_NAMES, "chessboard")
    gen = PipelineGenerator(seed)
    gen.generate_files()
    gen.run_pipeline(heuristic)

def main():
    args = set_env()
    if args['random']:
        random_pipeline()
    else:
        cfg = Config(args['map'])
        cfg.declare_content()
        problem = Problem(cfg)
        print("--- SOLVING PROBLEM ---")
        print('')
        print(f"Algorithm: {ALGORITHM_NAMES[args['algorithm']]}")
        if args['algorithm'] == "astar":
            print(f"Heuristic: {HEURISTIC_NAMES[args['heuristic']]}")
            print('')
            solver = Astar(problem, args['heuristic'])
            result = solver.solve_astar()
        elif args['algorithm'] == "bfs":
            print('')
            result = bfs(problem)
        elif args['algorithm'] == "dfs":
            print('')
            result = dfs(problem) 
        print_trace(*result, astar=(args['algorithm'] == "astar"))
if __name__ == "__main__":
    main()
