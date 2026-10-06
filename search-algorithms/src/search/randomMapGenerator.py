import os
import numpy as np
from src.environment.constants import GENERATOR_SIZES, ALGORITHM_NAMES
from src.environment.config import Config, INPUT_DIR
from src.environment.problem import Problem
from src.environment.utils import extract_trace
from src.search.algorithms.astar import Astar
from src.search.algorithms.bfs import BFS
from src.search.algorithms.dfs import DFS
from pathlib import Path

OUTPUT_DIR = Path(__file__).resolve().parents[2] / "output"

class PipelineGenerator:
    """
    Generates random maps and runs all the search algorithms on them.
    """

    def __init__(self, seed):
        """
        Creates the input and output folders and the random number generator.
        The attribute self.seed holds the numpy random generator built from the given seed.

        Args:
            seed (int): Seed of the random number generator.
        """
        self.files_dir = INPUT_DIR / "random"
        os.makedirs(self.files_dir, exist_ok= True)
        os.makedirs(OUTPUT_DIR, exist_ok= True)
        self.seed = np.random.default_rng(seed)

                
    def generate_files(self):
        """
        Creates the random map files: 5 maps for each size in GENERATOR_SIZES.
        """
        print('')
        print(f"--- CREATING FILES ---")
        print('')

        for size in GENERATOR_SIZES:
            for matrix in self.generator_func(size):
                self.create_input_file(size, *matrix)

        
    def generator_func(self, size):
        """
        Generates 5 random square maps of the given size.

        Args:
            size (int): Side of the square maps.

        Yields:
            tuple: (matrix, index), where matrix (np.ndarray) holds hardness values from 1 to 9
                and index (int) is the number of the map, from 0 to 4.
        """
        for i in range(0, 5):
            yield (self.seed.integers(low = 1, high = 10, size=(size, size)), i)

            
    def create_input_file(self, size, matrix, index):
        """
        Writes a map file with the start at (0, 0) facing North and the goal in the opposite
        corner with a random orientation from 0 to 8.

        Args:
            size (int): Side of the square map.
            matrix (np.ndarray): Hardness values of the map.
            index (int): Number of the map, used in the file name.
        """
        file_name = f"randomMap{size}x{size}_{index}.txt"
        file_path = self.files_dir / file_name

        with open(file_path, 'w') as file:
            sizeAux = f"{size} {size}"
            start = f"0 0 0"
            goal = f"{size-1} {size-1} {self.seed.integers(0, 9)}"
            matrixStr = [" ".join(map(str, row)) for row in matrix]

            for line in [sizeAux, *matrixStr, start, goal]:
                file.write(f"{line}\n")

            print(f"Created file {file_name}")
            print('')

            
    def extract_metrics(self, size, metrics_list, heuristic = None):
        """
        Builds the text with the mean depth, cost, explored nodes and frontier nodes of each algorithm.

        Args:
            size (str): Map size label shown in the header.
            metrics_list (dict): Maps each algorithm key ("bfs", "dfs", "astar") to the list of
                (depth, cost, explored, frontier) tuples obtained, one per map.
            heuristic (str, optional): Heuristic name shown in the A* header.

        Returns:
            str: Text with the mean metrics of every algorithm.
        """
        lines = [f"--- METRICS EXTRACTION FOR {size} ---", ""]

        for algorithm in metrics_list:
            if algorithm == "astar":
                lines.append(f"--- Metrics for algorithm {ALGORITHM_NAMES[algorithm]} ({heuristic}) ---")
            else:
                lines.append(f"--- Metrics for algorithm {ALGORITHM_NAMES[algorithm]} ---")

            metrics = np.mean(metrics_list[algorithm], axis= 0)
            lines.append(f"Mean depth: {metrics[0]}")
            lines.append(f"Mean Cost: {metrics[1]}")
            lines.append(f"Mean Explored Nodes: {metrics[2]}")
            lines.append(f"Mean Frontier Nodes: {metrics[3]}")
            lines.append("")
            lines.append('--------------------------------------------------------------')

        return "\n".join(lines) + "\n"

    
    def node_to_metrics(self, result):
        """
        Extracts the metrics of a search result.

        Args:
            result (tuple): Result of a search: (solution, last, n_explored, n_frontier).

        Returns:
            tuple: (depth, cost, n_explored, n_frontier) of the solution.
        """
        solution, _, n_explored, n_frontier = result
        return (solution.depth, solution.g, n_explored, n_frontier)


    def run_pipeline(self, heuristic):
        """
        Solves every generated map with BFS, DFS and A*. 
        Writes the traces and the mean metrics of each size to the files pipeline_generator_traces.txt 
        and pipeline_generator_metrics.txt in the output folder.

        Args:
            heuristic (str): Heuristic used by A*.
        """
        traces_path = OUTPUT_DIR / "pipeline_generator_traces.txt"
        metrics_path = OUTPUT_DIR / "pipeline_generator_metrics.txt"

        with open(traces_path, 'w') as traces_file:
            with open(metrics_path, 'w') as metrics_file:
                
                for size in GENERATOR_SIZES:
                    metrics = {"bfs": [], "dfs": [], "astar": []} 

                    for index in range(5):
                        map_name = f"random/randomMap{size}x{size}_{index}"
                        print(f"--- SOLVING {map_name} WITH BFS, DFS AND A*({heuristic}) ---")
                        print('')
                        cfg = Config(map_name)
                        problem = Problem(cfg)
                        dfs_solver = DFS(problem)
                        dfs_result = dfs_solver.solve_dfs()
                        metrics['dfs'].append(self.node_to_metrics(dfs_result))
                        bfs_solver = BFS(problem)
                        bfs_result = bfs_solver.solve_bfs()
                        metrics['bfs'].append(self.node_to_metrics(bfs_result))
                        solver = Astar(problem, heuristic)
                        astar_result = solver.solve_astar()
                        metrics['astar'].append(self.node_to_metrics(astar_result))
                        dfs_trace = extract_trace(map_name, ALGORITHM_NAMES['dfs'], *dfs_result)
                        bfs_trace = extract_trace(map_name, ALGORITHM_NAMES['bfs'], *bfs_result)
                        astar_trace = extract_trace(map_name, f"{ALGORITHM_NAMES['astar']} ({heuristic})", *astar_result, True)
                        
                        for trace in (bfs_trace, dfs_trace, astar_trace):
                            traces_file.write(trace + "\n")

                    metrics_file.write(self.extract_metrics(f"{size}x{size}", metrics, heuristic))