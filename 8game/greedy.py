
""" heapq
The heapq module in Python is part of the standard library and provides an implementation of the heap queue algorithm, also known as the priority queue algorithm
"""
import heapq

""" Greedy Best-First Algorithm 
Implementation of the Greedy Best-First Algorithm function, having as parameters the initial_state, final_state and heuristic taken as inputs in the main function, on index.py
"""
def greedy_best_first_search(initial_state, final_state, heuristic):
    """ Heuristic Selection
    Selects the heuristic function based on the 'heuristic' parameter. If manhattan is chosen, it uses the manhattan_distance function. Otherwise, it uses hamming_distance
    It is mandatory in the main function, on index.py, to chose either.
    """
    heuristic_function = manhattan_distance if heuristic == 'manhattan' else hamming_distance
    """ Variables/Data Structures Initialization
    - frontier - empty list named that will be used as a priority queue to store states to be explored, along with their heuristic values
    - heapq.heappush(...) - adds the initial state to the frontier with a heuristic value of 0, marking the starting point of the search
    - explored_nodes - is a set that stores the states that have already been visited to prevent revisiting
    - prev - is a dictionary mapping each state to the state that led to it, helping to reconstruct the path once the final state is found
    - max_depth
    """
    frontier = [] 
    heapq.heappush(frontier, (0, initial_state))
    explored_nodes = set() 
    prev = {tuple(map(tuple, initial_state)): None}

    """ Greddy BF Loop 
    The loop will continue as long as there are states in the 'frontier' to be explored
    """
    while frontier:
        """ Lowest Heuristic Value 
        Removes and returns the state from the frontier with the lowest heuristic value. 
        This is considered the current state for this iteration of the loop
        """
        current_heuristic, board = heapq.heappop(frontier)
        """ Final State Check
        If the current state is the goal state, the function reconstructs the path from the initial state to the final state using the 'prev' dictionary and returns it
        """
        if board == final_state:
            return reconstruct_path(board, prev)

        """ Mark as Explored
        Adds the current state to the 'explored_nodes' set to mark it as explored
        """
        explored_nodes.add(tuple(map(tuple, board)))

        """ Neighbor Exploration
        For each valid move (or 'neighbor') from the current state
        """
        for neighbor in neighbors(board):
            """ Exploration Check
            It checks if the neighbor hasn't been explored yet
            """
            if tuple(map(tuple, neighbor)) not in explored_nodes:
                """ Neighbor Addition
                The neighbor is added for exploration, marked as explored and current state is recorded as the neighbor's predecessor
                Adds the neighbor to the frontier along with its heuristic value calculated by the selected heuristic function. This value estimates the cost or distance from the neighbor to the goal state.
                """
                explored_nodes.add(tuple(map(tuple, neighbor)))
                prev[tuple(map(tuple, neighbor))] = tuple(map(tuple, board)) 
                heapq.heappush(frontier, (heuristic_function(neighbor, final_state), neighbor))

    return None 

""" Manhattan Distance
Calculates the total Manhattan distance between the current state and the goal state for all tiles except the empty tile (0). The Manhattan distance between two points is the sum of the absolute differences of their Cartesian coordinates - in this case, the row and column indices of the tiles.
It takes the current state and the final_state as parameters
"""
def manhattan_distance(state, final_state):
    distance = 0
    """ Distance Calculation
    These nested for loops iterate over every tile in the 'state' matrix. i and j are the row and column indices
    It then checks if the current tile is not the empty tile. If it is, it is not included for calculation
    Finds the target position (goal_i and goal_j) of the current tile in the final state. It does this by iterating over every tile in the final_state until it finds a tile matching the current tile's value. The next function returns the first matching coordinate.
    """
    for i in range(len(state)):
        for j in range(len(state[i])):
            if state[i][j] != 0: 
                goal_i, goal_j = next((x, y) for x, row in enumerate(final_state) for y, val in enumerate(row) if val == state[i][j])
                distance += abs(goal_i - i) + abs(goal_j - j)
    return distance

""" Hamming Distance
Calculates the number of tiles in the wrong position when comparing the current state to the goal state, excluding the empty tile
It takes the current state and the final_state as parameters
"""
def hamming_distance(state, final_state):
    distance = 0
    """ Distance Calculation
    These nested for loops iterate over every tile in the 'state' matrix. i and j are the row and column indices
    It then checks two conditions for each tile: that it is not the empty tile, and that its value does not match the corresponding tile's value in the final_state. This identifies tiles that are in the wrong position.
    Increments distance by 1 for each tile found to be in the wrong position.
    """
    for i in range(len(state)):
        for j in range(len(state[i])):
            if state[i][j] != 0 and state[i][j] != final_state[i][j]:
                distance += 1
    return distance

def neighbors(state):
    """ Find the Empty Tile
    It finds the coordinates (row, column) of the empty space
    enumerate(state) gives us a pair of (index, row), where 'index' is the row number and 'row' is the list representing the row in the puzzle
    row.index(0) finds the column index of the empty space('0') in the row
    This information is used to determine which moves are possible
    """
    empty_tile_position = [(i, row.index(0)) for i, row in enumerate(state) if 0 in row][0]
    
    neighbors = []

    """ Possible Moves (up, down, left, right)
    This list defines the directions in which the empty tile can move: down, up, right, and left, respectively.
    Each move is a tuple representing the change in the row and column of the empty space if that move is made.
    """
    moves = [(1, 0), (-1, 0), (0, 1), (0, -1)]

    """For each move possible"""
    for move in moves:
        new_row = empty_tile_position[0] + move[0]
        new_col = empty_tile_position[1] + move[1]

        """ Validate Move
        This checks if the move is valid by ensuring the new position of the empty space is still within the bounds of the grid
        """
        if 0 <= new_row < len(state) and 0 <= new_col < len(state[0]):
            """ Create New State 
            A new state is created as a copy of the current state. The : is used to create a shallow copy of each row so that we don't alter the original state
            """
            neighbor_state = [row[:] for row in state]
            """ Execute Move
            The value at the new position of the empty space (which will be a numbered tile after the move) is moved to where the empty space was
            The new position of the empty space is set to '0'
            """
            neighbor_state[empty_tile_position[0]][empty_tile_position[1]] = neighbor_state[new_row][new_col]
            neighbor_state[new_row][new_col] = 0
            """ Record Neighbor State
            This modified 'neighbor_state' is added to the list 'neighbors', signifying it's a valid state reachable from the current state
            """
            neighbors.append(neighbor_state)

    """ Return Neighbors
    The function returns the list 'neighbors', which contains all the new states that can be reached with one move from the current state
    """
    return neighbors

""" Reconstruct Path
Used to traceback the path from the goal state to the initial state once a solution has been found using the DFS algorithm. It works by utilizing the information stored in the 'prev' dictionary, which holds the predecessors of each state visiting during the search
It takes two parameters (state and prev)
"""
def reconstruct_path(state, prev):
    path = []
    """ Tracing Back the Path 
    The function enters a loop that will continue until there is no previous state to go back to, which happens when the initial state is reached and its 'prev' entry is 'None'
    """
    while state is not None:
        """ Append the Current State to the Path
        The current state is added to the path list. In the first iteration, this is the goal state, and in subsequent iterations, it will be each predecessor state leading back to the initial state.
        """
        path.append(state)
        """ Move to the Previous State 
        The current state is updated to its predecessor state. This is done by looking up the current state in the prev dictionary.
        Since lists are not hashable and cannot be used as keys in a dictionary, the state, which is a list of lists, is converted to a tuple of tuples. Tuples are hashable and can be used as keys.
        prev.get() is a safe way of retrieving the predecessor state from the dictionary; if the key doesn't exist, it returns None. (and the while loop ends)
        """
        state = prev.get(tuple(map(tuple, state)))
    """ Return the Reversed Path """
    return path[::-1]


