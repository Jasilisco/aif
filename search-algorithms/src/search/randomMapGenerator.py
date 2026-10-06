import numpy as np
import os
from src.environment.constants import GENERATOR_SIZES, ALGORITHM_NAMES
from src.environment.config import Config, INPUT_DIR
from src.environment.problem import Problem
from src.environment.utils import extract_trace
from src.search.algorithms.astar import Astar
from src.search.algorithms.sbf import bfs
from src.search.algorithms.sdf import dfs
from pathlib import Path

OUTPUT_DIR = Path(__file__).resolve().parents[2] / "output"

class PipelineGenerator:
    def __init__(self, seed):
        self.files_dir = INPUT_DIR / "random"
        os.makedirs(self.files_dir, exist_ok= True)
        os.makedirs(OUTPUT_DIR, exist_ok= True)
        self.seed = np.random.default_rng(seed)
                
    def generate_files(self):
        print('')
        print(f"--- CREATING FILES ---")
        print('')
        for size in GENERATOR_SIZES:
            for matrix in self.generator_func(size):
                self.create_input_file(size, *matrix)
        
    def generator_func(self, size):
        for i in range(0, 5):
            yield (self.seed.integers(low = 1, high = 10, size=(size, size)), i)
            
    def create_input_file(self, size, matrix, index):
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
        solution, _, n_explored, n_frontier = result
        return (solution.depth, solution.g, n_explored, n_frontier)

    def run_pipeline(self, heuristic):
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
                        dfs_result = dfs(problem)
                        metrics['dfs'].append(self.node_to_metrics(dfs_result))
                        bfs_result = bfs(problem)
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