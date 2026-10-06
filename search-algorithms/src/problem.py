# Row, column offset when advancing, indexed by orientation
MOVES = [
    (-1, 0), (-1, 1), (0, 1), (1, 1),
    (1, 0), (1, -1), (0, -1), (-1, -1)
]


def is_goal(state, goal):
    # Goal orientation 8 means the final orientation is irrelevant
    if state[0] != goal[0] or state[1] != goal[1]:
        return False

    return goal[2] == 8 or state[2] == goal[2]

#Devuelve lista de (operador, nuevo_estado, coste).
def successors(state, matrix):
    x, y, o = state
    result = []
    nx, ny = x + MOVES[o][0], y + MOVES[o][1]

    if 0 <= nx < len(matrix) and 0 <= ny < len(matrix[0]):
        result.append(("Advance", (nx, ny, o), int(matrix[nx][ny])))

    result.append(("RotateCW", (x, y, (o + 1) % 8), 1))
    result.append(("RotateCCW", (x, y, (o - 1) % 8), 1))

    return result