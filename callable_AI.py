def Connect_Four(DepthPlayer1, DepthPlayer2, row_count, col_count):
    import numpy as np
    import random
    import math
    import time

    # basic values that are uses repeatedly

    # row and column size
    ROW_COUNT = row_count
    COLUMN_COUNT = col_count

    EMPTY = 0

    # player/AI piece number
    PLAYER_PIECE = 1
    AI_PIECE = 2

    # size of window that get checked for score
    WINDOW_LENGTH = 4

    # this function creates the board for connect_Four
    def create_board():
        board = np.zeros((ROW_COUNT, COLUMN_COUNT))
        return board

    # this function places a piece on the board
    def placeAPiece(board, row, col, piece):
        board[row][col] = piece

    # this function checks if col is avaliable
    def rowDrop(board, col):
        return board[ROW_COUNT - 1][col] == 0

    # this function gives the next avaliable row in selected col
    def nextOpenRow(board, col):
        for r in range(ROW_COUNT):
            if board[r][col] == 0:
                return r

    # this function checks the board if there is a winner
    def winningMove(board, piece):
        # Check horizontal locations for win
        for c in range(COLUMN_COUNT - 3):
            for r in range(ROW_COUNT):
                # checks column to the right for same piece until length is 4(win)
                if board[r][c] == piece and board[r][c + 1] == piece and board[r][c + 2] == piece and board[r][
                    c + 3] == piece:
                    return True

        # Check vertical locations for win
        for c in range(COLUMN_COUNT):
            for r in range(ROW_COUNT - 3):
                # checks row higher for same piece until length is 4(win)
                if board[r][c] == piece and board[r + 1][c] == piece and board[r + 2][c] == piece and board[r + 3][c] == piece:
                    return True

        # Check positively sloped diaganols
        for c in range(COLUMN_COUNT - 3):
            for r in range(ROW_COUNT - 3):
                # checks row higher + col to the right for same piece until length is 4(win)
                if board[r][c] == piece and board[r + 1][c + 1] == piece and board[r + 2][c + 2] == piece and board[r + 3][
                    c + 3] == piece:
                    return True

        # Check negatively sloped diaganols
        for c in range(COLUMN_COUNT - 3):
            for r in range(3, ROW_COUNT):
                # checks row lower + colomn to the right for same piece until length is 4(win)
                if board[r][c] == piece and board[r - 1][c + 1] == piece and board[r - 2][c + 2] == piece and board[r - 3][
                    c + 3] == piece:
                    return True


    def evaluate_window(window, piece):
        score = 0
        opp_piece = PLAYER_PIECE
        # check to see what piece is the opponent
        if piece == PLAYER_PIECE:
            opp_piece = AI_PIECE

        # there are 4 pieces in window
        if window.count(piece) == 4:
            score += 100
        # there are 3 pieces and one empty in the window
        elif window.count(piece) == 3 and window.count(EMPTY) == 1:
            score += 5
        # there are 2 pieces and 2 empty in the window
        elif window.count(piece) == 2 and window.count(EMPTY) == 2:
            score += 2
        # there are 3 opponent pieces and one empty in the window
        if window.count(opp_piece) == 3 and window.count(EMPTY) == 1:
            score -= 4
        return score


    # evaluates the board and gives a score back(higher is beter)
    def score(board, piece):
        score = 0
        ## Score center column
        center_array = [int(i) for i in list(board[:, COLUMN_COUNT // 2])]
        center_count = center_array.count(piece)
        score += center_count * 3

        # Score Horizontal
        for r in range(ROW_COUNT):
            row_array = [int(i) for i in list(board[r, :])]
            for c in range(COLUMN_COUNT - 3):
                # puts array in window of 4 to be scored
                window = row_array[c:c + WINDOW_LENGTH]
                score += evaluate_window(window, piece)

        # Score Vertical
        for c in range(COLUMN_COUNT):
            col_array = [int(i) for i in list(board[:, c])]
            for r in range(ROW_COUNT - 3):
                # puts array in window of 4 to be scored
                window = col_array[r:r + WINDOW_LENGTH]
                score += evaluate_window(window, piece)

        # Score posiive sloped diagonal
        for r in range(ROW_COUNT - 3):
            for c in range(COLUMN_COUNT - 3):
                # puts array in window of 4 to be scored
                window = [board[r + i][c + i] for i in range(WINDOW_LENGTH)]
                score += evaluate_window(window, piece)

        for r in range(ROW_COUNT - 3):
            for c in range(COLUMN_COUNT - 3):
                # puts array in window of 4 to be scored
                window = [board[r + 3 - i][c + i] for i in range(WINDOW_LENGTH)]
                score += evaluate_window(window, piece)

        return score


    # this function checks the board if there is a winner
    def endOfGame(board):
        return winningMove(board, PLAYER_PIECE) or winningMove(board, AI_PIECE) or len(validLocations(board)) == 0

    # this function uses minimax to determan the next move to make
    def minimax(board, depth, maximizingPlayer):
        # basic value to be used
        valid_locations = validLocations(board)
        terminal = endOfGame(board)

        # end statment
        if depth == 0 or terminal:
            if terminal:
                if winningMove(board, AI_PIECE):
                    return (None, 100000000000000)
                elif winningMove(board, PLAYER_PIECE):
                    return (None, -10000000000000)
                else:
                    return (None, 0)
                # depth == 0
            else:
                return (None, score(board, AI_PIECE))

        if maximizingPlayer:
            best_score = -math.inf
            column = random.choice(valid_locations)
            # pick a random locations and repeat until depth 0 or terminal is reached
            for col in valid_locations:
                row = nextOpenRow(board, col)
                b_copy = board.copy()
                placeAPiece(b_copy, row, col, AI_PIECE)
                new_score = minimax(b_copy, depth - 1, False)[1]

                # set new score if new_score is higher the best_score
                if new_score > best_score:
                    best_score = new_score
                    column = col
            return column, best_score

        else:  # Minimizing player
            best_score = math.inf
            column = random.choice(valid_locations)
            # pick a random locations and repeat until depth 0 or terminal is reached
            for col in valid_locations:
                row = nextOpenRow(board, col)
                b_copy = board.copy()
                placeAPiece(b_copy, row, col, PLAYER_PIECE)
                new_score = minimax(b_copy, depth - 1, True)[1]

                # set new score if new_score is higher the best_score
                if new_score < best_score:
                    best_score = new_score
                    column = col
            return column, best_score

    # this function get the usable location on the board
    def validLocations(board):
        valid_locations = []
        for col in range(COLUMN_COUNT):
            if rowDrop(board, col):
                valid_locations.append(col)
        return valid_locations

    # this fucntion draws a simple board layout to the terminal
    def simple_draw_board(board):
        for row in np.flip(board):
            print(row)

    # this functino lets a person play the game
    def player_move(board):
        loc = validLocations(board)
        loc.reverse()
        print(loc)
        get_input = int(input("choose your column: "))
        nextOpenRow(board,get_input)
        placeAPiece(board,nextOpenRow(board,get_input) , get_input, PLAYER_PIECE)
        return True

    # this fucntion uses a randomizer to determan the next move
    def random_player(board):
        validLocations(board)
        col = random.choice(validLocations(board))
        row = nextOpenRow(board, col)
        placeAPiece(board, row, col, PLAYER_PIECE)

    # this function actives the AI_player
    def AI_player(board, level , piece): # level gaat expoinenteel meer tijd kosten per level
        mini_max = minimax(board, level, True)
        col = mini_max[0]
        validLocations(board)
        row = nextOpenRow(board, col)
        placeAPiece(board, row, col, piece)
        return col

    board = create_board()
    game_over = False
    turn = AI_PIECE
    start_time = time.time()
    turns = 0
    while not game_over:
        terminal = endOfGame(board)
        simple_draw_board(board)
        print("   next move   ")
        if terminal:
            game_over = True
            end_time = time.time()
            if winningMove(board, AI_PIECE):
                print("Winner is AI!")
                return 1, turns, end_time-start_time
            elif winningMove(board, PLAYER_PIECE):
                print("Winner is Player!")
                return 2, turns, end_time-start_time
            else:
                print("Tie!")
                return 0, turns, end_time - start_time

        if turn == AI_PIECE:
            AI_player(board,DepthPlayer1, AI_PIECE)
            turn = PLAYER_PIECE
        else:
            AI_player(board,DepthPlayer2, PLAYER_PIECE)
            turn = AI_PIECE
        turns += 1

Connect_Four(4,2,6,7)

