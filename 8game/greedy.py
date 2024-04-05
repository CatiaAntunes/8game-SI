
import heapq

""" Greedy Best-First Algorithm 
Implementation of the Greedy Best-First Algorithm function, having as parameters the initial_state and final_state taken as inputs in the main function, on index.py
"""
def greedy_best_first_search(initial_state, final_state, heuristic='manhattan'):
    heuristic_function = manhattan_distance if heuristic == 'manhattan' else hamming_distance
    frontier = [] 
    heapq.heappush(frontier, (0, initial_state))
    explored_nodes = set() 
    prev = {tuple(map(tuple, initial_state)): None}

    while frontier:
        current_heuristic, state = heapq.heappop(frontier)
        if state == final_state:
            return reconstruct_path(state, prev)

        explored_nodes.add(tuple(map(tuple, state)))

        for neighbor in neighbors(state):
            neighbor_tuple = tuple(map(tuple, neighbor))
            if neighbor_tuple not in explored_nodes:
                explored_nodes.add(neighbor_tuple)
                prev[neighbor_tuple] = tuple(map(tuple, state)) 
                heapq.heappush(frontier, (heuristic_function(neighbor, final_state), neighbor))

    return None 

def manhattan_distance(state, final_state):
    distance = 0
    for i in range(len(state)):
        for j in range(len(state[i])):
            if state[i][j] != 0: 
                goal_i, goal_j = next((x, y) for x, row in enumerate(final_state) for y, val in enumerate(row) if val == state[i][j])
                distance += abs(goal_i - i) + abs(goal_j - j)
    return distance

def hamming_distance(state, final_state):
    distance = 0
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


