import random
import bfs 
import dfs

def generate_random_matrix():
    matrix = random.sample(range(1, 9), 8)
    matrix.insert(7, 0)  # Insert 0 for the empty space
    return [matrix[i:i+3] for i in range(0, len(matrix), 3)]

def insert_manual_matrix():
    while True:
        try:
            user_input = input("Enter the matrix (without repetitions, separated by commas): ")
            numbers = [int(num) for num in user_input.split(",")]
            if len(numbers) != 8 or len(set(numbers)) != 8:
                raise ValueError("Please enter exactly 8 different numbers.")
            numbers.append(0)  # Add 0 for the empty space
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
    else:
        print("No solution found.")
elif choice == "2":
    print("Solving the puzzle using DFS...")
    path = dfs.dfs_algorithm(initial_matrix, final_matrix)
    if path is not None:
        print("Solution found:")
        for step, state in enumerate(path):
            print("Step", step + 1)
            print_puzzle(state)
    else:
        print("No solution found.")
elif choice == "3":
    pass
else:
    print("Invalid choice. Please choose one of the provided options.")
