# Name: [Your Name]
# Roll No: [Your Roll Number]
# BS Data Science - Fall 2024 (Afternoon)
# AI Lab 1 - Task 2
# Topic: Solving 15-Puzzle using A* Search with different heuristics

import heapq
import copy
import time
import math


class PuzzleNode:
    def __init__(self, state, parent, move, g_cost, h_cost):
        self.state = state
        self.parent = parent   # parent node (to trace path later)
        self.move = move       # what move was made to reach this state
        self.g_cost = g_cost   # cost from start to this node
        self.h_cost = h_cost   # heuristic estimate to goal
        self.f_cost = g_cost + h_cost  # total estimated cost

    def generate_children(self, goal_state, heuristic_type):
        n = len(self.state)
        children = []

        # find blank tile
        blank_r, blank_c = 0, 0
        for i in range(n):
            for j in range(n):
                if self.state[i][j] == 0:
                    blank_r = i
                    blank_c = j

        direction_names = {
            (-1, 0): "Up",
            (1, 0):  "Down",
            (0, -1): "Left",
            (0, 1):  "Right"
        }

        for dr, dc in direction_names:
            new_r = blank_r + dr
            new_c = blank_c + dc

            if 0 <= new_r < n and 0 <= new_c < n:
                new_state = copy.deepcopy(self.state)
                new_state[blank_r][blank_c] = new_state[new_r][new_c]
                new_state[new_r][new_c] = 0

                h = PuzzleNode.calculate_heuristic(new_state, goal_state, heuristic_type)
                child = PuzzleNode(
                    state=new_state,
                    parent=self,
                    move=direction_names[(dr, dc)],
                    g_cost=self.g_cost + 1,
                    h_cost=h
                )
                children.append(child)

        return children

    @staticmethod
    def calculate_heuristic(state, goal_state, heuristic_type="manhattan"):
        n = len(state)

        # build a map of where each tile should go in the goal
        goal_pos = {}
        for i in range(n):
            for j in range(n):
                goal_pos[goal_state[i][j]] = (i, j)

        # ---- Heuristic 1: Manhattan Distance ----
        # for each tile, count how many rows + columns it needs to travel
        if heuristic_type == "manhattan":
            total = 0
            for i in range(n):
                for j in range(n):
                    tile = state[i][j]
                    if tile != 0:
                        goal_r, goal_c = goal_pos[tile]
                        total += abs(i - goal_r) + abs(j - goal_c)
            return total

        # ---- Heuristic 2: Misplaced Tiles ----
        # just count how many tiles are not in their correct position
        elif heuristic_type == "misplaced_tiles":
            count = 0
            for i in range(n):
                for j in range(n):
                    if state[i][j] != 0 and state[i][j] != goal_state[i][j]:
                        count += 1
            return count

        # ---- Heuristic 3: Euclidean Distance ----
        # straight line distance from current position to goal position
        elif heuristic_type == "euclidean":
            total = 0.0
            for i in range(n):
                for j in range(n):
                    tile = state[i][j]
                    if tile != 0:
                        goal_r, goal_c = goal_pos[tile]
                        total += math.sqrt((i - goal_r)**2 + (j - goal_c)**2)
            return total

        # ---- Heuristic 4: Linear Conflict ----
        # manhattan distance + extra penalty for tiles that are in the right
        # row/column but in the wrong order (they have to pass each other)
        elif heuristic_type == "linear_conflict":
            # start with manhattan as base
            manhattan = PuzzleNode.calculate_heuristic(state, goal_state, "manhattan")
            conflicts = 0

            # check row conflicts
            for row in range(n):
                # get all tiles in this row that also belong in this row (goal-wise)
                row_tiles = []
                for col in range(n):
                    tile = state[row][col]
                    if tile != 0 and goal_pos[tile][0] == row:
                        row_tiles.append((col, goal_pos[tile][1]))  # (current col, goal col)

                # check every pair of such tiles
                for a in range(len(row_tiles)):
                    for b in range(a + 1, len(row_tiles)):
                        curr_a, goal_a = row_tiles[a]
                        curr_b, goal_b = row_tiles[b]
                        # if a is left of b now but should be right of b -> conflict
                        if curr_a < curr_b and goal_a > goal_b:
                            conflicts += 1
                        elif curr_a > curr_b and goal_a < goal_b:
                            conflicts += 1

            # check column conflicts
            for col in range(n):
                col_tiles = []
                for row in range(n):
                    tile = state[row][col]
                    if tile != 0 and goal_pos[tile][1] == col:
                        col_tiles.append((row, goal_pos[tile][0]))  # (current row, goal row)

                for a in range(len(col_tiles)):
                    for b in range(a + 1, len(col_tiles)):
                        curr_a, goal_a = col_tiles[a]
                        curr_b, goal_b = col_tiles[b]
                        if curr_a < curr_b and goal_a > goal_b:
                            conflicts += 1
                        elif curr_a > curr_b and goal_a < goal_b:
                            conflicts += 1

            # each conflict costs 2 extra moves minimum
            return manhattan + 2 * conflicts

        # ---- Heuristic 5: Max Heuristic ----
        # take the max of manhattan and misplaced tiles
        # a larger heuristic is better as long as it doesnt overestimate
        elif heuristic_type == "max_heuristic":
            h_manhattan = PuzzleNode.calculate_heuristic(state, goal_state, "manhattan")
            h_misplaced = PuzzleNode.calculate_heuristic(state, goal_state, "misplaced_tiles")
            return max(h_manhattan, h_misplaced)

        return 0

    def __lt__(self, other):
        # this is needed so heapq can compare nodes
        return self.f_cost < other.f_cost


class PuzzleSolver:
    def __init__(self, start_state, goal_state):
        self.start_state = start_state
        self.goal_state = goal_state

    def is_solvable(self, state):
        flat = []
        for row in state:
            for tile in row:
                if tile != 0:
                    flat.append(tile)

        n = len(state)

        inversions = 0
        for i in range(len(flat)):
            for j in range(i + 1, len(flat)):
                if flat[i] > flat[j]:
                    inversions += 1

        if n % 2 == 1:
            return inversions % 2 == 0
        else:
            blank_row_from_bottom = 0
            for i in range(n - 1, -1, -1):
                if 0 in state[i]:
                    blank_row_from_bottom = n - i
                    break
            return (inversions + blank_row_from_bottom) % 2 == 1

    def astar_search(self, heuristic_type="manhattan"):
        nodes_expanded = 0

        # calculate heuristic for starting state
        start_h = PuzzleNode.calculate_heuristic(self.start_state, self.goal_state, heuristic_type)
        start_node = PuzzleNode(
            state=self.start_state,
            parent=None,
            move="Start",
            g_cost=0,
            h_cost=start_h
        )

        # open list is a priority queue - always pops lowest f_cost first
        open_list = []
        heapq.heappush(open_list, start_node)

        # closed set stores states we already explored
        visited = set()

        while open_list:
            current = heapq.heappop(open_list)
            nodes_expanded += 1

            state_key = tuple(tuple(row) for row in current.state)

            # skip if already visited
            if state_key in visited:
                continue
            visited.add(state_key)

            # check if we reached the goal
            if current.state == self.goal_state:
                return current, nodes_expanded

            # generate children and add to open list
            for child in current.generate_children(self.goal_state, heuristic_type):
                child_key = tuple(tuple(row) for row in child.state)
                if child_key not in visited:
                    heapq.heappush(open_list, child)

        return None, nodes_expanded

    def trace_solution(self, node):
        # follow parent pointers from goal back to start
        path = []
        while node is not None:
            path.append((node.move, node.state))
            node = node.parent

        path.reverse()  # reverse so it goes from start to goal

        print(f"  Total moves: {len(path) - 1}")
        for i, (move, state) in enumerate(path):
            print(f"  Step {i} - {move}:")
            for row in state:
                line = ""
                for tile in row:
                    if tile == 0:
                        line += "  _  "
                    else:
                        line += f"{tile:3}  "
                print(" ", line)
            print()


# -----------------------------------------------
# Sample run (as given in lab sheet)
# -----------------------------------------------

initial_state = [[1, 2, 3, 4],
                 [5, 6, 7, 8],
                 [9, 10, 11, 12],
                 [13, 14, 0, 15]]

goal_state = [[1, 2, 3, 4],
              [5, 6, 7, 8],
              [9, 10, 11, 12],
              [13, 14, 15, 0]]

solver = PuzzleSolver(initial_state, goal_state)

if solver.is_solvable(initial_state):
    print("The puzzle is solvable. Proceeding with A* Search...\n")

    # list of all heuristics to test
    heuristics = [
        ("manhattan",       "Manhattan Distance"),
        ("misplaced_tiles", "Misplaced Tiles"),
        ("euclidean",       "Euclidean Distance"),
        ("linear_conflict", "Linear Conflict"),
        ("max_heuristic",   "Max Heuristic"),
    ]

    results = []

    for htype, hname in heuristics:
        print(f"Running A* Search ({hname})...")
        start_time = time.time()
        solution, nodes_expanded = solver.astar_search(heuristic_type=htype)
        end_time = time.time()

        if solution:
            print(f"\nSolution ({hname}):")
            solver.trace_solution(solution)
            print(f"Execution Time: {end_time - start_time:.5f} seconds")
            print(f"Nodes Expanded: {nodes_expanded}\n")
            results.append((hname, solution.g_cost, nodes_expanded, end_time - start_time))
        else:
            print("No solution found.\n")

    # performance comparison table
    print("=" * 65)
    print("              PERFORMANCE COMPARISON (A* Heuristics)")
    print("=" * 65)
    print(f"{'Heuristic':<30} {'Moves':>6}  {'Nodes Expanded':>15}  {'Time (s)':>10}")
    print("-" * 65)
    for hname, moves, nodes, t in results:
        print(f"{hname:<30} {moves:>6}  {nodes:>15}  {t:>10.5f}")
    print("=" * 65)

else:
    print("The puzzle is NOT solvable.")