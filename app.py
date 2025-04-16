import chess


def get_node_value(board):
    """
    This is used to get the value/score of the node with respect to white
    :param board:
    :return: Value of board based on amounts of pieces of white vs amount of pieces of black
    """

    # We first give each value to each piece of the board
    values_of_pieces = {
        chess.PAWN:3,
        chess.KNIGHT:6,
        chess.BISHOP:6,
        chess.ROOK:12,
        chess.QUEEN:24,
        chess.KING:0
    }

    # This is whites total score
    total_score = 0

    # We loop over every box of the chess board and increase/decrease value based on piece and its color white(+) black(-)
    for box in chess.SQUARES:
        piece = board.piece_at(box)
        if piece is None: # If that box is empty
            continue
        else: # if the box is not empty
            value = values_of_pieces[piece.piece_type]
            if piece.color == chess.WHITE:
                total_score += value
            else:
                total_score -= value
    return total_score


def alpha_beta_prunning(board,alpha,beta,isMax,levels):
    """

    :param board: State of board
    :param alpha: Alpha value
    :param beta: Beta value
    :param isMax: Seeing if current node is maximum true if it is and false if it isnt
    :return:
    """
    if board.is_game_over() or levels == 0:
        return get_node_value(board)

    if isMax:
        max_value = -float('inf') # Basically give - infinity value which is initial value of alpha
        # Now we see for all the legal moves that are allowed and simulate each one
        for move in board.legal_moves:
            board.push(move) # Simulate the legal move
            get_value = alpha_beta_prunning(board,alpha,beta,False,levels-1)
            board.pop() # Undo the move that was made previously
            max_value = max(max_value,get_value) # Update node value
            alpha = max(alpha,get_value) # update alpha value

            #Check condition for pruning
            if alpha>= beta:
                break
        return max_value # The value that alpha node selected is returned
    else:
        min_value = float('inf')# Basically give postive infinity value which is initial value of beta
        for move in board.legal_moves:
            board.push(move)  # Simulate the legal move
            get_value = alpha_beta_prunning(board, alpha, beta, True, levels - 1)
            board.pop()  # Undo the move that was made previously
            min_value = min(min_value, get_value)  # Update node value
            beta = min(beta, get_value)  # update alpha value

            # Check condition for pruning
            if alpha >= beta:
                break
        return min_value  # The value that alpha node selected is returned

def get_best_move(board,levels):

    #Find the best move with respect to black

    move_to_take = None
    curr_val = float('inf')

    for move in board.legal_moves:
        board.push(move)
        # Since black has already made the move, white will try to maximize its value
        white_val = alpha_beta_prunning(board,-float('inf'),float('inf'),True,levels)
        board.pop()
        # Here if the value of white is decreasing this means this is the move that black should take
        if curr_val > white_val:
            curr_val = white_val
            move_to_take = move
    return move_to_take



"""
ACTUAL GAME STARTS HERE
"""

#Intialize board
board = chess.Board()

# Depths to search in alpha beta prunning
levels = 2
players_moves = []
bots_moves = []
# While the game is not over keep running
while not board.is_game_over():
    print(board.unicode(borders=True,invert_color=True))
    print()
    print("Players move: ",players_moves)
    print("Bots move: ", bots_moves)
    print()
    # If it's players turn
    if board.turn == chess.WHITE:
        move = input("Enter your move in UCI format (e.g e2e4 which means take piece e2 to e4): ")
        try:
            #Convert move from string to Move which is for the chess library

            move = chess.Move.from_uci(move)

        except:
            print("Invalid move try again")
            continue
        # if the move is not possible then make the player do the move again
        if move not in board.legal_moves:
            print("Invalid move. Please try again.")
            continue
        players_moves.append(move.uci())
        board.push(move)
    else:
        # it is black's turn and it gets its best move using alpha beta pruning
        print('Computer is thinking....')
        move = get_best_move(board,levels)
        bots_moves.append(move.uci())
        board.push(move)
        print("Computer played it's move ", move)
        print()

print(board.mirror().unicode(borders=True,invert_color=True))
if board.is_checkmate():
    if board.turn == chess.WHITE:
        print("Black wins due to checkmate!!")
    else:
        print("White wins due to checkmate")
elif board.is_stalemate():
    print("Match is a draw due to stalemate")
else:
    print("Game over.")
