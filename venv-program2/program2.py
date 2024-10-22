# Intro to AI - Program 2

# Driver program takes in 2 inputs: executable of program 1 and executable of naive program
# - Outputs the entire grid

# Naive program  
# How it works: 
# given the grid from the driver, it finds all the possible moves that it can play 
# -> appends it to an array of moves
# -> from that moves array, randomly chooses a move and excutes it
# -> sends this state to the driver 

# Program 1
# Design: 

# Check for Immediate Wins or Blocks:
# Before invoking Minimax, always check if there is an immediate move that results in a win.
# Similarly, block the opponent from winning by preventing them from completing four in a row.

# Minimax Algorithm: 
# - This algorithm simulates all possible future game states by recursively evaluating each possible move.
# For each move, simulate the game and evaluate the outcome (win, loss, or draw).
# If the move results in a win, assign a high score.
# If the move leads to a loss, assign a low score.
# Use recursive depth-limited search to prevent excessive computation (search for 4 or 5 moves ahead).
# Return the move that gives the best score.

# Alpha-Beta Pruning:
# To optimize Minimax, alpha-beta pruning reduces the number of states evaluated by cutting off unnecessary branches in the game tree.
# This allows the player to go deeper in fewer moves and increases efficiency.


import json
import sys

player = int(sys.argv[2])
width = int(sys.argv[4])
height = int(sys.argv[6])

def valid_moves(state):
    # check for all current valid moves from the current state 
    # return as a list of integers 
    grid = state['grid']
    moves = []
    # iterate through all the columns 
    for i in range(width):
        # check if the top row of the column is empty, if it is then its a valid move
        if grid[i][0] == 0:  
            moves.append(i)
    return moves

def check_win(grid, player):
    # check for all winning conditions for the player
    # iterate through each cell in the grid
    for i in range(width):
        for j in range(height):
            # if the current cell belongs to the player, check each direction for 4 in a row
            if grid[i][j] == player:
                if check_direction(grid, i, j, 1, 0, player) or \
                   check_direction(grid, i, j, 0, 1, player) or \
                   check_direction(grid, i, j, 1, 1, player) or \
                   check_direction(grid, i, j, 1, -1, player):
                   #If any direction contains 4 consecutive pieces of the same player, return True
                    return True
    return False

def check_direction(grid, x, y, dx, dy, player):
    count = 0
    for i in range(4):
        # ff within bounds and belongs to the player, increment count
        nx, ny = x + i * dx, y + i * dy
        if 0 <= nx < width and 0 <= ny < height and grid[nx][ny] == player:
            count += 1
        else:
            break
    # return True if there are 4 in a row
    return count == 4

def minimax(state, depth, alpha, beta, maximizingPlayer):
    """
    Minimax algorithm with alpha-beta pruning.
    - `state`: current game state
    - `depth`: depth limit for the search (limits the search tree depth)
    - `alpha`: best value the maximizing player can guarantee
    - `beta`: best value the minimizing player can guarantee
    - `maximizingPlayer`: True if it's the AI's turn to maximize score, False if it's the opponent's turn to minimize score
    """

    # Get the list of valid moves
    valid = valid_moves(state)
    # if depth is 0, no valid moves, or someone has won
    if depth == 0 or len(valid) == 0 or check_win(state['grid'], player) or check_win(state['grid'], 3 - player):
        # Return evaluation of current state
        return evaluate_state(state)
    
    if maximizingPlayer:
        # maximizing player wants the highest score
        maxEval = -float('inf')
        for move in valid:
            # simulate making a move for the maximizing player
            new_state = make_move(state, move, player)
            # recursively evaluate the move
            eval = minimax(new_state, depth-1, alpha, beta, False)
            maxEval = max(maxEval, eval)
            # update alpha (best score found so far)
            alpha = max(alpha, eval)
            if beta <= alpha:
                # prune the search if alpha >= beta
                break
        return maxEval
    else:
        # minimizing player wants the lowest score
        minEval = float('inf')
        for move in valid:
            # simulate making a move for the opponent/minimizing player
            new_state = make_move(state, move, 3 - player)
            # recursively evaluate the move
            eval = minimax(new_state, depth-1, alpha, beta, True)
            minEval = min(minEval, eval)
            # update beta (best score minimizing player can achieve)
            beta = min(beta, eval)
            if beta <= alpha:
                # prune the search if beta <= alpha
                break
        return minEval

def make_move(state, move, player):
    # Copy the grid to avoid modifying the original state
    grid = [list(col) for col in state['grid']]
    for i in range(height-1, -1, -1):
        if grid[move][i] == 0:
            grid[move][i] = player
            break
    # Return the new state with the updated grid
    new_state = {'grid': grid, 'player': player}
    return new_state

def evaluate_state(state):
    # looks at the grid state for the current player
    grid = state['grid']
    if check_win(grid, player):
        return float('inf')  # current player wins
    elif check_win(grid, 3 - player):
        return -float('inf')  # opponent wins
    else:
        # Heuristic score based on the number of potential winning lines
        return score_position(grid, player) - score_position(grid, 3 - player)


# Calculate a score for the current position based on potential winning lines
def score_position(grid, player):
    # score the grid position based on potential winning lines for the player
    score = 0
    for i in range(width):
        for j in range(height):
            if grid[i][j] == player:
                # score vertical, horizontal, and diagonal lines
                score += count_direction(grid, i, j, 1, 0, player)  # vertical
                score += count_direction(grid, i, j, 0, 1, player)  # horizontal
                score += count_direction(grid, i, j, 1, 1, player)  # diagonal /
                score += count_direction(grid, i, j, 1, -1, player) # diagonal \
    return score


# Count the number of aligned pieces in a specified direction
def count_direction(grid, x, y, dx, dy, player):
    # count potential for winning in a direction (dx, dy)
    count = 0
    for i in range(4):
        nx, ny = x + i * dx, y + i * dy
        if 0 <= nx < width and 0 <= ny < height and (grid[nx][ny] == player or grid[nx][ny] == 0):
            count += 1
        else:
            break
    return count

for line in sys.stdin:
    state = json.loads(line)
    best_move = -1
    best_value = -float('inf')
    
    for move in valid_moves(state):
        new_state = make_move(state, move, player)
        move_value = minimax(new_state, 4, -float('inf'), float('inf'), False)
        if move_value > best_value:
            best_value = move_value
            best_move = move
    
    action = {'move': best_move}
    msg = json.dumps(action)
    sys.stdout.write(msg + '\n')
    sys.stdout.flush()
