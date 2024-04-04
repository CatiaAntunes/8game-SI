from collections import deque

def dfs_algorithm(initial_state, final_state):
    stack = [initial_state]
    explored_nodes = set()
    prev = {}  # Dictionary to store the previous state for each state
    max_depth = 0

    while stack:
        board = stack.pop()
        explored_nodes.add(tuple(map(tuple, board)))  # Convert lists to tuples
        if board == final_state:
            return reconstruct_path(board, prev)
        for neighbor in neighbors(board):
            if tuple(map(tuple, neighbor)) not in explored_nodes:
                stack.append(neighbor)
                explored_nodes.add(tuple(map(tuple, neighbor)))
                prev[tuple(map(tuple, neighbor))] = tuple(map(tuple, board))  # Store the previous state
                max_depth = max(max_depth, len(neighbor))
    return None

def neighbors(state):
    # Find the position of the empty tile (0)
    empty_tile_position = [(i, row.index(0)) for i, row in enumerate(state) if 0 in row][0]
    neighbors = []

    # Define possible moves (up, down, left, right)
    moves = [(1, 0), (-1, 0), (0, 1), (0, -1)]

    for move in moves:
        new_row = empty_tile_position[0] + move[0]
        new_col = empty_tile_position[1] + move[1]

        # Check if the new position is within the bounds of the puzzle
        if 0 <= new_row < len(state) and 0 <= new_col < len(state[0]):
            # Create a copy of the current state
            neighbor_state = [row[:] for row in state]
            # Swap the empty tile with the adjacent tile
            neighbor_state[empty_tile_position[0]][empty_tile_position[1]] = neighbor_state[new_row][new_col]
            neighbor_state[new_row][new_col] = 0
            neighbors.append(neighbor_state)

    return neighbors

def reconstruct_path(state, prev):
    path = []
    while state is not None:
        path.append(state)
        state = prev.get(tuple(map(tuple, state)))  # Get the previous state from the dictionary
    return path[::-1]