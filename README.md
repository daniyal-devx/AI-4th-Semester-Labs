# 🤖 Artificial Intelligence — 4th Semester Labs

> **BS Data Science | FAST-NUCES | Fall 2024**  
> Search Algorithms • Game AI • Evolutionary Computing • Machine Learning

---

## 👤 Author

**Daniyal Usman**  
Roll No: BSDSF24A025  
Program: BS Data Science (Fall 2024, Afternoon)  
GitHub: [@daniyal-devx](https://github.com/daniyal-devx)

---

## 📋 Labs Overview

| # | Lab | Topics Covered | Files |
|---|-----|---------------|-------|
| 01 | **Puzzle Solving — Search Algorithms** | IDDFS, A* with 5 heuristics | `Lab-01/` |
| 02 | **Game AI — Adversarial Search** | Minimax, Alpha-Beta Pruning | `Lab-02/` |
| 03 | **Evolutionary Computing** | Genetic Algorithms, Knapsack, TSP | `Lab-03/` |
| 04 | **Supervised Learning** | Decision Tree, Random Forest | `Lab-04/` |

---

## 🔬 Lab Details

### Lab 01 — Puzzle Solving with Search Algorithms

**Task 1 — IDDFS (Iterative Deepening DFS)**
- Solves the classic **15-Puzzle** using Depth-First Iterative Deepening
- Implements solvability check using inversion count
- Generates and explores all valid moves from blank tile

**Task 2 — A\* Search with Multiple Heuristics**
- Solves the same puzzle using **informed search**
- Implements and compares **5 heuristic functions**:
  | Heuristic | Description |
  |-----------|-------------|
  | Manhattan Distance | Sum of row + column distances per tile |
  | Misplaced Tiles | Count of tiles not in goal position |
  | Euclidean Distance | Straight-line distance to goal |
  | Linear Conflict | Manhattan + penalty for conflicting tile pairs |
  | Max Heuristic | `max(Manhattan, Misplaced)` |
- Outputs performance table: moves, nodes expanded, time

---

### Lab 02 — Game AI with Adversarial Search

**Task 1 — Minimax Algorithm**
- Implements full **Minimax** for Tic-Tac-Toe
- AI plays as 'O', human plays as 'X'
- Tested at depths 2, 4, and 9 with node count + timing comparison

**Task 2 — Alpha-Beta Pruning**
- Optimizes Minimax with **Alpha-Beta Pruning** to cut unnecessary branches
- Same Tic-Tac-Toe setup but significantly fewer nodes evaluated
- Side-by-side performance comparison with Minimax

---

### Lab 03 — Genetic Algorithms

**Task 1 — Knapsack Problem**
- 30 items, capacity = 60 units
- Binary chromosome representation (1 = selected, 0 = not)
- Supports both **Roulette Wheel** and **Tournament Selection**
- 50 generations, mutation rate = 0.05

**Task 2 — Travelling Salesman Problem (TSP)**
- 8 cities with 2D coordinates
- Permutation chromosome (city visit order)
- Uses **Order Crossover (OX)** to maintain valid routes
- Swap mutation, 100 generations
- Supports user-defined city count and coordinates

---

### Lab 04 — Supervised Machine Learning

**Dataset:** Loan Approval (Analytics Vidhya)

**Task 1 — Decision Tree Classifier**
- Tested at depths: 2, 5, and None (unlimited)
- Metrics: Accuracy, Precision, Recall
- Demonstrates overfitting at unlimited depth

**Task 2 — Random Forest**
- Tested with: 10, 50, and 100 estimators
- Compared against Decision Tree on same metrics
- Shows ensemble advantage over single tree

---

## 🛠️ Tech Stack

```
Python 3.x
├── Standard Library: heapq, math, copy, random, time
└── External Libraries:
    ├── pandas
    └── scikit-learn
```

---

## 🚀 How to Run

### Prerequisites
```bash
pip install pandas scikit-learn
```

### Lab 01
```bash
cd Lab-01
python BSDSF24A025_Lab_01_Task_01.py   # IDDFS
python BSDSF24A025_Lab_01_Task_02.py   # A* Search
```

### Lab 02
```bash
cd Lab-02
python Lab_02_task1_minimax.py          # Minimax
python Lab_02_task2_alphabeta.py        # Alpha-Beta Pruning
```

### Lab 03
```bash
cd Lab-03
python task1_knapsack.py                # Genetic Algorithm - Knapsack
python task2_tsp.py                     # Genetic Algorithm - TSP
```

### Lab 04
```bash
cd Lab-04
# Place CSV files in the same directory first
python BSDSF24A025_LAB-04.py
```

> **Note for Lab 04:** The following dataset files must be in the `Lab-04/` folder:
> - `train_u6lujuX_CVtuZ9i.csv`
> - `test_Y3wMUE5_7gLdaTN.csv`

---

## 📁 Repository Structure

```
AI-4th-Semester-Labs/
│
├── README.md
│
├── Lab-01/
│   ├── BSDSF24A025_Lab_01_Task_01.py     # IDDFS
│   └── BSDSF24A025_Lab_01_Task_02.py     # A* with heuristics
│
├── Lab-02/
│   ├── Lab_02_task1_minimax.py            # Minimax
│   ├── Lab_02_task2_alphabeta.py          # Alpha-Beta Pruning
│   └── tictactoe_ai.py                    # Standalone TicTacToe
│
├── Lab-03/
│   ├── task1_knapsack.py                  # GA - Knapsack
│   └── task2_tsp.py                       # GA - TSP
│
└── Lab-04/
    ├── BSDSF24A025_LAB-04.py              # Decision Tree + Random Forest
    ├── train_u6lujuX_CVtuZ9i.csv          # Training data
    ├── test_Y3wMUE5_7gLdaTN.csv           # Test data
    └── my_submission.csv                   # Predictions
```

---

## 📊 Key Results

| Lab | Algorithm | Highlight |
|-----|-----------|-----------|
| 01 | A* (Linear Conflict) | Fewest nodes expanded among all heuristics |
| 02 | Alpha-Beta vs Minimax | ~60-80% reduction in nodes at depth 9 |
| 03 | GA - TSP | Converges to near-optimal route in ~100 generations |
| 04 | Random Forest (100 trees) | Best accuracy vs single Decision Tree |

---

## 🏷️ Topics

`artificial-intelligence` `search-algorithms` `a-star` `minimax` `alpha-beta-pruning`
`genetic-algorithms` `machine-learning` `decision-tree` `random-forest` `python`
`jupyter-notebook` `bs-data-science` `FAST-NUCES`

---

*Course: Artificial Intelligence | Instructor: [Instructor Name] | Spring 2026*
