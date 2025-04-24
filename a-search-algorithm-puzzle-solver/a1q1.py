import heapq
import random
import copy
import pandas as pd

GOAL_STATE = [[1, 2, 3], [4, 5, 6], [7, 8, 0]]  # 0 represents the empty tile

#Helper function to print a puzzle state.
def print_puzzle(puzzle):
    for row in puzzle:
        print(row)
    print()

#Find the position of a tile in the puzzle.
def find_position(puzzle, value):
    for i, row in enumerate(puzzle):
        if value in row:
            return i, row.index(value)

#Heuristic h1: Misplaced tiles.
def misplaced_tiles(puzzle):
    return sum(1 for i in range(3) for j in range(3) if puzzle[i][j] != 0 and puzzle[i][j] != GOAL_STATE[i][j])

#Heuristic h2: Manhattan distance.
def manhattan_distance(puzzle):
    distance = 0
    for i in range(3):
        for j in range(3):
            value = puzzle[i][j]
            if value != 0:
                x_goal, y_goal = find_position(GOAL_STATE, value)
                distance += abs(i - x_goal) + abs(j - y_goal)
    return distance

#Heuristic h3: Linear conflict.
def linear_conflict(puzzle):
    linear_conflict = manhattan_distance(puzzle)
    for i in range(3):
        for j in range(3):
            tile = puzzle[i][j]
            if tile != 0 and find_position(GOAL_STATE, tile)[0] == i:
                for k in range(j + 1, 3):
                    if puzzle[i][k] != 0 and find_position(GOAL_STATE, puzzle[i][k])[0] == i and puzzle[i][k] < tile:
                        linear_conflict += 2
            if tile != 0 and find_position(GOAL_STATE, tile)[1] == j:
                for k in range(i + 1, 3):
                    if puzzle[k][j] != 0 and find_position(GOAL_STATE, puzzle[k][j])[1] == j and puzzle[k][j] < tile:
                        linear_conflict += 2
    return linear_conflict

#Generate n unique solvable puzzles.
def generate_reachable_puzzles(n=100):
    puzzles = set()
    print("Generating 100 unique, reachable puzzles...")
    while len(puzzles) < n:
        puzzle = generate_random_puzzle()
        puzzles.add(tuple(map(tuple, puzzle)))
    return [list(map(list, puzzle)) for puzzle in puzzles]

#Generate a random solvable puzzle state.
def generate_random_puzzle():
    puzzle = [1, 2, 3, 4, 5, 6, 7, 8, 0]
    while True:
        random.shuffle(puzzle)
        state = [puzzle[i:i + 3] for i in range(0, 9, 3)]
        if is_solvable(state):
            return state
        
#Check if the puzzle state is solvable.
def is_solvable(puzzle):
    flat_puzzle = [tile for row in puzzle for tile in row if tile != 0]
    inversions = sum(1 for i in range(len(flat_puzzle)) for j in range(i + 1, len(flat_puzzle)) if flat_puzzle[i] > flat_puzzle[j])
    return inversions % 2 == 0

#Perform A* search on a given puzzle using the specified heuristic.
def a_star(puzzle, heuristic):
    def get_neighbors(puzzle):
        neighbors = []
        x, y = find_position(puzzle, 0)
        moves = [(-1, 0), (1, 0), (0, -1), (0, 1)]  # Up, Down, Left, Right
        for dx, dy in moves:
            nx, ny = x + dx, y + dy
            if 0 <= nx < 3 and 0 <= ny < 3:
                new_puzzle = copy.deepcopy(puzzle)
                new_puzzle[x][y], new_puzzle[nx][ny] = new_puzzle[nx][ny], new_puzzle[x][y]
                neighbors.append(new_puzzle)
        return neighbors

    open_list = []
    heapq.heappush(open_list, (0 + heuristic(puzzle), 0, puzzle, None))
    visited = set()
    steps = 0
    nodes_expanded = 0

    while open_list:
        _, g, current, _ = heapq.heappop(open_list)
        steps += 1

        if current == GOAL_STATE:
            return g, nodes_expanded

        visited.add(tuple(map(tuple, current)))

        for neighbor in get_neighbors(current):
            if tuple(map(tuple, neighbor)) not in visited:
                nodes_expanded += 1
                heapq.heappush(open_list, (g + 1 + heuristic(neighbor), g + 1, neighbor, current))

    return -1, nodes_expanded

if __name__ == "__main__":
    puzzles = generate_reachable_puzzles(100)
    results = []  # Store all results

    for i, puzzle in enumerate(puzzles):
        print(f"Initial State for Puzzle {i + 1}:")
        print_puzzle(puzzle)

        h1_steps, h1_nodes = a_star(puzzle, misplaced_tiles)
        h2_steps, h2_nodes = a_star(puzzle, manhattan_distance)
        h3_steps, h3_nodes = a_star(puzzle, linear_conflict)

        print(f"Goal state achieved for Puzzle {i + 1}!\n")

        results.append({
            'Puzzle': i + 1,
            'Initial State': str(puzzle),
            'Steps (h1)': h1_steps, 'Nodes (h1)': h1_nodes,
            'Steps (h2)': h2_steps, 'Nodes (h2)': h2_nodes,
            'Steps (h3)': h3_steps, 'Nodes (h3)': h3_nodes
        })

    # Ensure full table display without truncation
    pd.set_option('display.max_rows', None)  # Show all rows
    pd.set_option('display.max_colwidth', None)  # Prevent column truncation

    df = pd.DataFrame(results)
    print(df)