import random
import bfs 
import dfs
import greedy
import time
import tracemalloc

""" Generate Random Matrix
Generates a random 3x3 matrix that represents the 8 game puzzle
"""
def generate_random_matrix():
    matrix = random.sample(range(0, 9), 9)
    return [matrix[i:i+3] for i in range(0, len(matrix), 3)]

""" Create Manual Matrix
Allows the user to manually input a 3x3 matrix. It validates the input to ensure it contains exactly nune different numbers between 0 and 9
"""
def insert_manual_matrix():
    while True:
        try:
            user_input = input("Enter the matrix (without repetitions, separated by commas, from 0 to 8): ")
            numbers = [int(num) for num in user_input.split(",")]
            if len(numbers) != 9 or len(set(numbers)) != 9:
                raise ValueError("Please enter exactly 9 different numbers.")
            return [numbers[i:i+3] for i in range(0, len(numbers), 3)]
        except ValueError as e:
            print(e)

""" Print Matrix
Prints any given matrix with a tile, formatting it neatly for the console
"""
def print_matrix(matrix, title):
    print(title)
    for row in matrix:
        print(" ".join(map(str, row)))

""" Print Puzzle
Similar to Print Matrix but formats numbers to be right-justified for a uniform appearance
"""
def print_puzzle(state):
    for row in state:
        print(" ".join(map(lambda x: str(x).rjust(2), row)))
    print()

""" Count Inversions
Counts the number of inversions in the puzzle.
Inversions are pairs of tiles that are in the reverse order from where they ought to be. This count is crucial to determine if the puzzle is solvable
"""
def count_inversions(sequence):
    inv_count = 0
    for i in range(len(sequence)):
        for j in range(i + 1, len(sequence)):
            if sequence[i] > sequence[j] and sequence[i] != 0 and sequence[j] != 0:
                inv_count += 1
    return inv_count

""" Solvable Puzzle ?
Determines if the puzzle can be solved by comparing the parity of inversions in the start and final matrices. Puzzles are solvable if and only if the start and final configurations have the same inversion parity.
"""
def is_solvable(start_matrix, goal_matrix):
    start_sequence = [tile for row in start_matrix for tile in row]
    goal_sequence = [tile for row in goal_matrix for tile in row]
    start_inversions = count_inversions(start_sequence)
    goal_inversions = count_inversions(goal_sequence)
    return (start_inversions % 2) == (goal_inversions % 2)

def print_info(start_time, end_time, peak, path):
    print(f"Max Memory Used (Peak):\t{round((peak/1048576),2)} MB")
    print(f"Execution Time:\t\t{round(end_time - start_time, 2)} seconds")
    print(f"Moves needed:\t\t{len(path)} moves")

""" Main Game Loop
The main game loop that orchestrates user interaction, matrix generation, algorithm selection, and solving the puzzle.
"""
def main_game():
    while True:
        """ Initial State Random or Manual """
        print("Select one of the following options for the initial matrix:")
        print("1. Generate initial matrix randomly")
        print("2. Insert initial matrix manually")
        print("--------------------")
        choice = input("Option: ")
        if choice == "1":
            initial_matrix = generate_random_matrix()
        elif choice == "2":
            initial_matrix = insert_manual_matrix()


        print("--------------------")

        """ Final State Random or Manual """
        print("Select one of the following options for the final matrix:")
        print("1. Generate final matrix randomly")
        print("2. Insert final matrix manually")
        print("--------------------")
        choice = input("Option: ")
        if choice == "1":
            final_matrix = generate_random_matrix()
        elif choice == "2":
            final_matrix = insert_manual_matrix()

        """ Print Both States"""
        print("--------------------")
        print_matrix(initial_matrix, "Initial Matrix")
        print("--------------------")
        print_matrix(final_matrix, "Final Matrix")


        print("--------------------")

        """ If Puzzle is Solvable, continue. Else check if the user wants to try a different combination of matrices """
        if is_solvable(initial_matrix, final_matrix):

            print("Puzzle is solvable. Proceed by choosing one algorithm...\n--------------------")

            """Algorithm Selection"""
            print("Select the algorithm you want to use to solve the puzzle:")
            print("1. BFS")
            print("2. DFS")
            print("3. Greedy Best First")
            print("--------------------")
            choice = input("Option: ")
            print("--------------------")
            
            """ Checks and executes (if valid) user's choice """
            # BFS
            if choice == "1":
                start_time = time.time()
                tracemalloc.start()
                print("Solving the puzzle using BFS...")
                path = bfs.bfs_algorithm(initial_matrix, final_matrix)
                current, peak = tracemalloc.get_traced_memory()  # Capture both current and peak memory
                tracemalloc.stop()  # Stop memory tracing
                end_time = time.time()
                if path is not None:
                    print("Solution found:")
                    for step, state in enumerate(path):
                        print("Step", step + 1)
                        print_puzzle(state)
                        print("")     
                print_info(start_time, end_time, peak, path)              
                break
            
            # DFS
            elif choice == "2":
                start_time = time.time()
                tracemalloc.start()
                print("Solving the puzzle using DFS...")
                path = dfs.dfs_algorithm(initial_matrix, final_matrix)
                current, peak = tracemalloc.get_traced_memory()  # Capture both current and peak memory
                tracemalloc.stop()  # Stop memory tracing
                end_time = time.time()
                if path is not None:
                    print("Solution found:")
                    for step, state in enumerate(path):
                        print("Step", step + 1)
                        print_puzzle(state)
                        print("")
                print_info(start_time, end_time, peak, path)
                break

            # Greedy BF
            elif choice == "3":
                # Heuristic Search
                while True:
                    print("Select the heuristic for the Greedy Best First Search:")
                    print("1. Manhattan Distance")
                    print("2. Hamming Distance")
                    heuristic_choice = input("Option: ")
                    if heuristic_choice == "1":
                        heuristic = "manhattan"
                        break
                    elif heuristic_choice == "2":
                        heuristic = "hamming"
                        break
                    else:
                        print("Invalid choice!")
                
                print(f"Solving the puzzle using Greedy Best First Search with {heuristic} heuristic...")
                start_time = time.time()
                tracemalloc.start()
                path = greedy.greedy_best_first_search(initial_matrix, final_matrix, heuristic)
                current, peak = tracemalloc.get_traced_memory()  # Capture both current and peak memory
                tracemalloc.stop()  # Stop memory tracing
                end_time = time.time()
                if path is not None:
                    print("Solution found:")
                    for step, state in enumerate(path):
                        print("Step", step + 1)
                        print_puzzle(state)
                        print("")
                print_info(start_time, end_time, peak, path)
                break
            else:
                print("Invalid choice. Please choose one of the provided options.\n")
        else:
            continue_game = True
            while True:
                not_solvable = input("Puzzle is not solvable. Do you want to try a different combination? (Y/N): ")
                if not_solvable.upper() == 'N':
                    continue_game = False
                    break
                elif not_solvable.upper() == 'Y':
                    break
                else:
                    print("Invalid response.\n")
            
            if continue_game == False:
                break

main_game()