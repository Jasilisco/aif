class Astar:
    
    def solve_astar(initial_state, goal, board):
        pass
        
    def chessboard_weighted_distance(start, goal, board):
        return int(board.min()) * max(abs(start[0] - goal[0]), abs(start[1] - goal[1]))