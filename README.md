# A* Puzzle Solver - Sliding Puzzle Search

Solves 8, 15 and 24 sliding puzzles with A* search, and compares three heuristics on how many nodes each one expands.

## At a Glance

- **Stack:** Python, pandas
- **Context:** CP 468 Artificial Intelligence, Wilfrid Laurier University (Assignment 1, Group 8)
- **State:** Complete

## Features

- A* search over 8, 15 and 24 puzzle boards
- Three heuristics: misplaced tiles, Manhattan distance, and linear conflict
- Runs 100 random puzzles per size: fully shuffled 8 and 24 puzzles, and 15 puzzles scrambled 30 moves from the goal
- Logs steps and nodes expanded per heuristic for side-by-side comparison

## How It Works

Each state is scored with `f(n) = g(n) + h(n)`, where `g` is moves so far and `h` is the heuristic. Linear conflict builds on Manhattan distance by adding a penalty when two tiles in the same row or column block each other, so it usually expands the fewest nodes of the three.

## Project Structure

```
a-search-algorithm-puzzle-solver/
├── a1q1.py                  # 8 puzzle
├── a1q2.py                  # 15 puzzle
├── a1q3.py                  # 24 puzzle
└── a-search-overview.pdf    # Write-up and heuristic performance analysis
```

## Running Locally

1. Clone the repo and move into the solver folder:
   ```bash
   git clone https://github.com/nakulpatel0306/a-search-puzzle-algorithm.git
   cd a-search-puzzle-algorithm/a-search-algorithm-puzzle-solver
   ```
2. Install pandas (used by the 8 and 24 puzzle scripts) and run a puzzle size:
   ```bash
   pip install pandas
   python3 a1q1.py
   ```

The 8 puzzle run finishes in about a minute. The 15 puzzle run (`a1q2.py`) takes much longer. The 24 puzzle run (`a1q3.py`) fully shuffles each board, which plain A* can't solve in practical time, and its solvability check is wrong for odd-width boards, so treat it as reference code rather than something to run to completion.

## Team

Romin Gandhi, Jenish Bharucha, Nakul Patel, Arsh Patel, Dhairya Patel, Paarth Bagga, Devarth Trivedi, Gleb Silin, Emmet Currie, Parker Riches

Built as coursework for CP 468 at Wilfrid Laurier University. Please do not copy for academic submissions.
