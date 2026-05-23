# Name: [Your Name]
# Roll No: [Your Roll Number]
# BS Data Science - Fall 2024 (Afternoon)
# AI Lab 1 - Task 1
# Topic: Solving 15-Puzzle using IDDFS

import copy
import time


class Puzzle:
    def __init__(self, initial_state, goal_state):
        self.initial_state = initial_state
        self.goal_state = goal_state

    def is_solvable(self, state):
        # flatten the grid and ignore the blank tile (0)
        flat = []
        for row in state:
            for tile in row:
                if tile != 0:
                    flat.append(tile)

        n = len(state)

        # count inversions
        # an inversion is when a bigger number appears before a smaller one
        inversions = 0
        for i in range(len(flat)):
            for j in range(i + 1, len(flat)):
                if flat[i] > flat[j]:
                    inversions += 1

        if n % 2 == 1:
            # for odd grid size, solvable if inversions is even
            return inversions % 2 == 0
        else:
            # for even grid size, find which row the blank is in (from bottom)
            blank_row_from_bottom = 0
            for i in range(n - 1, -1, -1):
                if 0 in state[i]:
                    blank_row_from_bottom = n - i
                    break
            # solvable if (inversions + blank row from bottom) is odd
            return (inversions + blank_row_from_bottom) % 2 == 1

    def generate_moves(self, state):
        # find where the blank tile (0) is
        n = len(state)
        blank_r, blank_c = 0, 0
        for i in range(n):
            for j in range(n):
                if state[i][j] == 0:
                    blank_r = i
                    blank_c = j

        # blank can move up, down, left, right
        directions = [(-1, 0), (1, 0), (0, -1), (0, 1)]
        moves = []

        for dr, dc in directions:
            new_r = blank_r + dr
            new_c = blank_c + dc

            # check if new position is within grid
            if 0 <= new_r < n and 0 <= new_c < n:
                new_state = copy.deepcopy(state)
                # swap blank with the neighboring tile
                new_state[blank_r][blank_c] = new_state[new_r][new_c]
                new_state[new_r][new_c] = 0
                moves.append(new_state)

        return moves

    def depth_limited_search(self, state, depth, visited):
        # if we reached the goal state, return path containing just this state
        if state == self.goal_state:
            return [state]

        # if depth limit reached and not at goal, return nothing
        if depth == 0:
            return None

        # convert state to tuple so we can store it in a set
        state_key = tuple(tuple(row) for row in state)
        visited.add(state_key)

        for next_state in self.generate_moves(state):
            next_key = tuple(tuple(row) for row in next_state)

            if next_key not in visited:
                result = self.depth_limited_search(next_state, depth - 1, visited)
                if result is not None:
                    # prepend current state to the solution path
                    return [state] + result

        # backtrack - remove current state from visited
        visited.discard(state_key)
        return None

    def iddfs(self):
        # first check if its solvable at all
        if not self.is_solvable(self.initial_state):
            return None

        # keep increasing depth limit until we find the solution
        for depth_limit in range(0, 200):
            visited = set()
            result = self.depth_limited_search(self.initial_state, depth_limit, visited)
            if result is not None:
                return result

        return None


def print_state(state):
    for row in state:
        line = ""
        for tile in row:
            if tile == 0:
                line += "  _ "
            else:
                line += f"{tile:3} "
        print(line)
    print()


def run_test(name, initial_state, goal_state):
    print(f"--- {name} ---")
    print("Initial State:")
    print_state(initial_state)

    puzzle = Puzzle(initial_state, goal_state)

    if puzzle.is_solvable(initial_state):
        print("Solvability Check: SOLVABLE")
        start = time.time()
        solution = puzzle.iddfs()
        end = time.time()

        if solution:
            print(f"Solution found in {len(solution) - 1} move(s)")
            print(f"Time taken: {end - start:.5f} seconds\n")
            print("Solution Path:")
            for i, state in enumerate(solution):
                print(f"Step {i}:")
                print_state(state)
        else:
            print("No solution found.\n")
    else:
        print("Solvability Check: NOT SOLVABLE")
        print("Skipping search.\n")


# -----------------------------------------------
# main
# -----------------------------------------------

goal_state = [[1, 2, 3, 4],
              [5, 6, 7, 8],
              [9, 10, 11, 12],
              [13, 14, 15, 0]]

# test case from lab sheet
initial_state = [[1, 2, 3, 4],
                 [5, 6, 7, 8],
                 [9, 10, 11, 12],
                 [13, 14, 0, 15]]

puzzle = Puzzle(initial_state, goal_state)
print("IDDFS Solution:", puzzle.iddfs())

print("\n========================================")
print("        Running All Test Cases")
print("========================================\n")

# solvable test case - 1 move away
run_test(
    "Test 1: Solvable (1 move)",
    [[1, 2, 3, 4], [5, 6, 7, 8], [9, 10, 11, 12], [13, 14, 0, 15]],
    goal_state
)

# solvable test case - few more moves
run_test(
    "Test 2: Solvable (2 moves)",
    [[1, 2, 3, 4], [5, 6, 7, 8], [9, 10, 0, 12], [13, 14, 11, 15]],
    goal_state
)

# unsolvable - 14 and 15 are swapped
run_test(
    "Test 3: Unsolvable",
    [[1, 2, 3, 4], [5, 6, 7, 8], [9, 10, 11, 12], [13, 15, 14, 0]],
    goal_state
)