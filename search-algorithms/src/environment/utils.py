def path_to(node):
    path = []
    while node is not None:
        path.append(node)
        node = node.parent
    return list(reversed(path))

def format_node(node, astar = False):
    """
    (d, g(n), op, S) for blind search.
    (d, g(n), op, h(n), S) if the node has an 'h' attribute (A*).
    """
    op = node.operator if node.operator is not None else "-"
    
    if not astar:
        return f"({node.depth}, {node.g}, {op}, {node.state})"
    return f"({node.depth}, {node.g}, {op}, {node.h}, {node.state})"

def print_trace(solution, last, n_explored, n_frontier, astar= False):
    print('--- TRACE PRINTING ---')
    print('')
    if solution is None:
        print("No solution found. Path from the initial state to the last examined node:")
        print('')
        node = last
    else:
        node = solution
 
    path = path_to(node)
    n = len(path) - 1
 
    for i, current in enumerate(path):
        if i > 0:
            print(f"Operator {i}: {current.operator}")
        if i == 0:
            label = "Node 0 (starting node)"
        elif i == n and solution is not None:
            label = f"Node {i} (final node)"
        else:
            label = f"Node {i}"
        print(f"{label}: {format_node(current, astar)}")
        
    print('')
    print('--- TRACE INFORMATION PARAMS ---')
    print('')
    if solution is not None:
        print(f"Final depth: {node.depth}")
        print(f"Final cost: {node.g}")
    print(f"Total number of items in explored list: {n_explored}")
    print(f"Total number of items in frontier: {n_frontier}")
    print('')
    
    
def extract_trace(filename, algorithm, solution, last, n_explored, n_frontier, astar=False):
    lines = [f"--- TRACE PRINTING FOR {filename} WITH ALGORITHM {algorithm} ---", ""]

    if solution is None:
        lines += ["No solution found. Path from the initial state to the last examined node:", ""]
        node = last
    else:
        node = solution

    path = path_to(node)
    n = len(path) - 1

    for i, current in enumerate(path):
        if i > 0:
            lines.append(f"Operator {i}: {current.operator}")
        if i == 0:
            label = "Node 0 (starting node)"
        elif i == n and solution is not None:
            label = f"Node {i} (final node)"
        else:
            label = f"Node {i}"
        lines.append(f"{label}: {format_node(current, astar)}")

    lines += ["", "--- TRACE INFORMATION PARAMS ---", ""]
    if solution is not None:
        lines.append(f"Final depth: {node.depth}")
        lines.append(f"Final cost: {node.g}")
    lines.append(f"Total number of items in explored list: {n_explored}")
    lines.append(f"Total number of items in frontier: {n_frontier}")
    lines.append('--------------------------------------------------------------')

    return "\n".join(lines) + "\n"