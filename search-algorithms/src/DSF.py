import sys
import numpy

def DFS(inicio, goal, board):
    x0, y0, o0 = inicio
    xf, yf, of = goal
    
    init_pos = board[x0][y0]
    
    print(init_pos)
    
def DFS_recursivo(inicio, terreno):
    expandidos = set()
    pila = [inicio]
    
    while pila:
        nodo = pila.pop()
        if nodo not in expandidos:
            expandidos.add(nodo)
        