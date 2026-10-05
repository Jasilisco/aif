# Equivalence between input integer orientations and string orientations, just for content declaring purposes
ORIENTATIONS = {
    0: 'North',
    1: 'Northeast',
    2: 'East',
    3: 'Southeast',
    4: 'South',
    5: 'Southwest',
    6: 'West',
    7: 'Northwest',
    8: 'Irrelevant'
}

# Equivalence between the given orientation (matching the ORIENTATIONS dict) and the move that is allowed on that orientation
# Example, orientation 'Northwest'(7), can only move up-left, so to the current position (x, y) the move would be (x-1, y-1) 
MOVES = {
    0: (-1,  0), 
    1: (-1,  1), 
    2: (0,  1), 
    3: (1,  1),
    4: ( 1,  0), 
    5: ( 1, -1), 
    6: (0, -1), 
    7: (-1, -1),
}