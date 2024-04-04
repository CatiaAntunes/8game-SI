import random
import bfs 
import dfs

def generate_random_matrix():
    matrix = random.sample(range(0, 9), 9)
    #matrix.insert(7, 0)  # Insert 0 for the empty space
    return [matrix[i:i+3] for i in range(0, len(matrix), 3)]

def insert_manual_matrix():
    while True:
        try:
            user_input = input("Enter the matrix (without repetitions, separated by commas, from 0 to 8): ")
            numbers = [int(num) for num in user_input.split(",")]
            if len(numbers) != 9 or len(set(numbers)) != 9:
                raise ValueError("Please enter exactly 9 different numbers.")
            #numbers.append(0)  # Add 0 for the empty space
            return [numbers[i:i+3] for i in range(0, len(numbers), 3)]
        except ValueError as e:
            print(e)

def print_matrix(matrix, title):
    print(title)
    for row in matrix:
        print(" ".join(map(str, row)))

def print_puzzle(state):
    for row in state:
        print(" ".join(map(lambda x: str(x).rjust(2), row)))
    print()

def count_inversions(sequence):
    inv_count = 0
    for i in range(len(sequence)):
        for j in range(i + 1, len(sequence)):
            if sequence[i] > sequence[j] and sequence[i] != 0 and sequence[j] != 0:
                inv_count += 1
    return inv_count

def is_solvable(start_matrix, goal_matrix):
    start_sequence = [tile for row in start_matrix for tile in row]
    goal_sequence = [tile for row in goal_matrix for tile in row]
    start_inversions = count_inversions(start_sequence)
    goal_inversions = count_inversions(goal_sequence)
    # Check if the parity of the inversion count is the same for both start and goal
    return (start_inversions % 2) == (goal_inversions % 2)

def main_game():
    while True:
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


        print("Select one of the following options for the final matrix:")
        print("1. Generate final matrix randomly")
        print("2. Insert final matrix manually")
        print("--------------------")
        choice = input("Option: ")
        if choice == "1":
            final_matrix = generate_random_matrix()
        elif choice == "2":
            final_matrix = insert_manual_matrix()


        print("--------------------")
        print_matrix(initial_matrix, "Initial Matrix")
        print("--------------------")
        print_matrix(final_matrix, "Final Matrix")


        print("--------------------")

        if is_solvable(initial_matrix, final_matrix):
            print("Puzzle is solvable. Proceeding with the chosen algorithm...\n--------------------")

            # Algorithm selection
            print("Select the algorithm you want to use to solve the puzzle:")
            print("1. BFS")
            print("2. DFS")
            print("3. Greedy Best First")
            print("--------------------")
            choice = input("Option: ")
            print("--------------------")
            # Check the user's choice 
            if choice == "1":
                print("Solving the puzzle using BFS...")
                path = bfs.bfs_algorithm(initial_matrix, final_matrix)
                if path is not None:
                    print("Solution found:")
                    for step, state in enumerate(path):
                        print("Step", step + 1)
                        print_puzzle(state)
                        print("")
                break
            elif choice == "2":
                print("Solving the puzzle using DFS...")
                path = dfs.dfs_algorithm(initial_matrix, final_matrix)
                if path is not None:
                    print("Solution found:")
                    for step, state in enumerate(path):
                        print("Step", step + 1)
                        print_puzzle(state)
                        print("")
                break
            elif choice == "3":
                pass
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