from src.environment.config import Config, INPUT_DIR
from src.environment.problem import Problem
from src.environment.utils import print_trace
from src.environment.constants import ALGORITHM_NAMES, HEURISTIC_NAMES, SEED
from src.search.algorithms.astar import Astar
from src.search.algorithms.sbf import Sbf
from src.search.algorithms.sdf import Sdf
from src.search.randomMapGenerator import PipelineGenerator
import numpy as np

def pick_setting(title, parse, default=None, prompt="> "):
    """
    Asks the user for a value until a valid one is entered.

    Args:
        title (str): Text shown to the user.
        parse (Callable[[str], Any]): Converts the typed answer into the final value
        default (Any, optional): Value returned when the answer is empty. Defaults to None.
        prompt (str, optional): Prefix shown on the input line. Defaults to '> '.

    Returns:
        Any: The value returned by parse, or default if the answer was empty.
    """
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
    """
    Shows a numbered list of options and asks the user to pick one.

    Args:
        title (str): Question shown above the list of options.
        options (dict): Maps each option key to the text.
        default (Any, optional): Key returned when the answer is empty. Defaults to None.

    Returns:
        Any: The key of the selected option, or default if the answer was empty.
    """
    keys = list(options)
    for i, key in enumerate(keys, start=1):
        title += f"\n  {i}. {options[key]}"

    def parse(answer):
        """
        Converts the typed option number into its key.
        """
        if answer.isdigit() and 1 <= int(answer) <= len(keys):
            return keys[int(answer) - 1]
        raise ValueError(f"Please enter a number between 1 and {len(keys)}.")
    
    return pick_setting(title, parse, default)


def pipeline_seed(default=SEED):
    """
    Asks the user for the seed used to generate the random maps.

    Args:
        default (int, optional): Seed returned when the answer is empty. Defaults to SEED.

    Returns:
        int: The seed entered by the user.
    """
    def parse(answer):
        """
        Converts the typed answer into an integer seed.
        """
        if answer.isdigit():
            return int(answer)
        raise ValueError("Please enter a numeric seed.")
    
    return pick_setting(f"Enter a numeric seed (default: {default}):", parse, default)


def input_file():
    """
    Asks the user for the name of a map file in the input folder.

    Returns:
        str: Name of the chosen map.
    """
    available = sorted(p.stem for p in INPUT_DIR.glob("*.txt"))

    def parse(answer):
        """
        Checks that the typed name corresponds to an existing map file.
        """
        if not answer:
            raise ValueError("File name cannot be empty.")
        if not (INPUT_DIR / f"{answer}.txt").exists():
            raise ValueError(f"File not found: {answer}.txt")
        return answer
    
    return pick_setting(f"Input file:\n  Available maps: {', '.join(available)}",
               parse, prompt="  Enter name: ")


def set_env():
    """
    Asks the user for the execution mode, map, algorithm and heuristic.

    Returns:
        dict: Selected settings with the keys. In random mode, map, algorithm and heuristic are None.
    """
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
    """
    Generates 20 random maps and solves them with all the algorithms.

    Asks for the seed (fixed or random) and for the A* heuristic, then
    generates the map files and runs the comparison pipeline.
    """
    seed_choice = env_setting(
        "Would you like to set a seed for reproducibility purposes or use a random one? (default: random seed)",
        {1: "Select a seed", 2: "Use a random seed"},
        2,
    )
    if seed_choice == 1:
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
            solver = Sbf(problem)
            result = solver.solve_sbf()
        elif args['algorithm'] == "dfs":
            print('')
            solver = Sdf(problem)
            result = solver.solve_sdf() 
        print_trace(*result, astar=(args['algorithm'] == "astar"))


if __name__ == "__main__":
    main()