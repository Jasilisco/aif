def read_input(path):
    with open(path, 'r') as f:
        lines = f.readlines()
        return lines

def path_to(node):
    path = []
    while node is not None:
        path.append(node)
        node = node.parent
    return list(reversed(path))

def format_node(node):
    """
    (d, g(n), op, S) for blind search.
    (d, g(n), op, h(n), S) if the node has an 'h' attribute (A*).
    """
    op = node.operator if node.operator is not None else "-"
    h = getattr(node, "h", None)
    
    if h is None:
        return f"({node.depth}, {node.g}, {op}, {node.state})"
    return f"({node.depth}, {node.g}, {op}, {h}, {node.state})"

def print_trace(solution, last, n_explored, n_frontier):
    if solution is None:
        print("No solution found. Path from the initial state to the last examined node:")
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
        print(f"{label}: {format_node(current)}")
 
    print()
    print(f"Total number of items in explored list: {n_explored}")
    print(f"Total number of items in frontier: {n_frontier}")