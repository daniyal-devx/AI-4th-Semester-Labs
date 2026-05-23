import math
import time


WIN_CONDITIONS = [
    (0, 1, 2), (3, 4, 5), (6, 7, 8),
    (0, 3, 6), (1, 4, 7), (2, 5, 8),
    (0, 4, 8), (2, 4, 6)
]


def print_board(board):
    print(f"\n {board[0]} | {board[1]} | {board[2]}")
    print("---+---+---")
    print(f" {board[3]} | {board[4]} | {board[5]}")
    print("---+---+---")
    print(f" {board[6]} | {board[7]} | {board[8]}\n")


def check_winner(board, player):
    return any(all(board[i] == player for i in cond) for cond in WIN_CONDITIONS)


class Minimax:
    def __init__(self, game_state, max_depth=9):
        self.game_state = game_state
        self.max_depth = max_depth
        self.nodes_expanded = 0

    def is_terminal(self, state):
        return check_winner(state, 'O') or check_winner(state, 'X') or ' ' not in state

    def utility(self, state):
        if check_winner(state, 'O'):
            return 1
        if check_winner(state, 'X'):
            return -1
        return 0

    def heuristic(self, state):
        score = 0
        for cond in WIN_CONDITIONS:
            cells = [state[i] for i in cond]
            o = cells.count('O')
            x = cells.count('X')
            if x == 0:
                score += o
            elif o == 0:
                score -= x
        return score

    def minimax(self, state, depth, maximizing_player):
        self.nodes_expanded += 1

        if self.is_terminal(state):
            return self.utility(state)
        if depth == 0:
            return self.heuristic(state)

        if maximizing_player:
            best = -math.inf
            for i in range(9):
                if state[i] == ' ':
                    state[i] = 'O'
                    score = self.minimax(state, depth - 1, False)
                    state[i] = ' '
                    best = max(best, score)
            return best
        else:
            best = math.inf
            for i in range(9):
                if state[i] == ' ':
                    state[i] = 'X'
                    score = self.minimax(state, depth - 1, True)
                    state[i] = ' '
                    best = min(best, score)
            return best

    def best_move(self, state):
        self.nodes_expanded = 0
        best_score = -math.inf
        best_idx = None

        for i in range(9):
            if state[i] == ' ':
                state[i] = 'O'
                score = self.minimax(state, self.max_depth - 1, False)
                state[i] = ' '
                if score > best_score:
                    best_score = score
                    best_idx = i

        return best_idx


def main():
    board = [' ' for _ in range(9)]
    human_player = 'X'
    ai_player = 'O'
    current_player = human_player

    print("Testing Minimax at different depths:")
    test_board = ['X', 'O', 'X', ' ', 'O', ' ', ' ', 'X', ' ']
    print_board(test_board)

    for depth in [9, 4, 2]:
        ai = Minimax(test_board[:], max_depth=depth)
        start = time.time()
        move = ai.best_move(test_board[:])
        elapsed = time.time() - start
        print(f"Depth={depth} | Best Move: {move} | Nodes Expanded: {ai.nodes_expanded} | Time: {elapsed:.4f}s")

    print("\n--- Starting Game ---")
    ai = Minimax(board)

    while ' ' in board:
        print_board(board)
        if current_player == human_player:
            move = int(input(f"Enter your move (0-8): "))
            if board[move] == ' ':
                board[move] = human_player
                if check_winner(board, human_player):
                    print_board(board)
                    print("You win!")
                    return
                current_player = ai_player
            else:
                print("Invalid move, try again.")
        else:
            move = ai.best_move(board)
            board[move] = ai_player
            print(f"AI selects position {move}")
            if check_winner(board, ai_player):
                print_board(board)
                print("AI wins!")
                return
            current_player = human_player

    print_board(board)
    print("Game ended in a draw!")


if __name__ == "__main__":
    main()
