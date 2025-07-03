
X = "X"  # AI player
O = "O"  # Human player
EMPTY = " "

# Create initial empty board
def initial_state():
    return [EMPTY] * 9

# Return list of available actions (empty spots)
def actions(state):
    return [i for i in range(9) if state[i] == EMPTY]

# Return new state after applying an action
def result(state, action):
    new_state = state.copy()
    new_state[action] = current_player(state)
    return new_state

# Determine current player
def current_player(state):
    x_count = state.count(X)
    o_count = state.count(O)
    return X if x_count == o_count else O

# Check if the game has ended
def terminal(state):
    return winner(state) is not None or EMPTY not in state

# Return the winner if there is one
def winner(state):
    win_lines = [
        [0, 1, 2], [3, 4, 5], [6, 7, 8],  # rows
        [0, 3, 6], [1, 4, 7], [2, 5, 8],  # columns
        [0, 4, 8], [2, 4, 6]              # diagonals
    ]
    for line in win_lines:
        a, b, c = line
        if state[a] == state[b] == state[c] != EMPTY:
            return state[a]
    return None

# Return 1 if AI (X) wins, -1 if human (O) wins, 0 for draw
def utility(state):
    win = winner(state)
    if win == X:
        return 1
    elif win == O:
        return -1
    else:
        return 0

# Minimax functions
def max_value(state):
    if terminal(state):
        return utility(state)
    v = -1000000000
    for action in actions(state):
        v = max(v, min_value(result(state, action)))
    return v

def min_value(state):
    if terminal(state):
        return utility(state)
    v = 1000000000
    for action in actions(state):
        v = min(v, max_value(result(state, action)))
    return v

# Find the best move for AI (X)
def best_move(state):
    best_score = -1000000000
    move = None
    for action in actions(state):
        score = min_value(result(state, action))
        if score > best_score:
            best_score = score
            move = action
    return move


def play_game():
    state = initial_state()
    while not terminal(state):
        print_board(state)
        if current_player(state) == O:
            move = int(input("Enter your move (1-9): ")) - 1
            if move not in actions(state):
                print("Invalid move.")
                continue
        else:
            print("AI is thinking...")
            move = best_move(state)
        state = result(state, move)

    print_board(state)
    if winner(state):
        print("Winner:", winner(state))
    else:
        print("It's a draw!")

def print_board(state):
    print()
    print(f"{state[0]} | {state[1]} | {state[2]}")
    print("--+---+--")
    print(f"{state[3]} | {state[4]} | {state[5]}")
    print("--+---+--")
    print(f"{state[6]} | {state[7]} | {state[8]}")
    print()


play_game()