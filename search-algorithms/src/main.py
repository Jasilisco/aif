from config import Config
import sys
import DSF as dsf

def main():
    if len(sys.argv) < 2:
        raise Exception("The name of the input file must be providen")
    
    mapa = Config(sys.argv[1])
    
    inicio = mapa.start_state()
    objetivo = mapa.goal_state()
    board = mapa.board
    
    print(inicio, objetivo, board)
    
    dsf.DFS(inicio, objetivo, board)
    
   

if __name__ == "__main__":
    main()