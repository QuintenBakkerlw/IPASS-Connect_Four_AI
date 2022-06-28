import time
import tkinter as tk
import numpy as np
import random
import math

# basic values that are uses repeatedly

# row and column size
ROW_COUNT = 6
COLUMN_COUNT = 7

EMPTY = 0

# player/AI piece number
PLAYER_PIECE = 1
AI_PIECE = 2
DEPTH_PLAYER_1 = 4

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
            if board[r][c] == piece and board[r + 1][c] == piece and board[r + 2][c] == piece and board[r + 3][
                c] == piece:
                return True

    # Check positively sloped diaganols
    for c in range(COLUMN_COUNT - 3):
        for r in range(ROW_COUNT - 3):
            # checks row higher + col to the right for same piece until length is 4(win)
            if board[r][c] == piece and board[r + 1][c + 1] == piece and board[r + 2][c + 2] == piece and \
                    board[r + 3][
                        c + 3] == piece:
                return True

    # Check negatively sloped diaganols
    for c in range(COLUMN_COUNT - 3):
        for r in range(3, ROW_COUNT):
            # checks row lower + colomn to the right for same piece until length is 4(win)
            if board[r][c] == piece and board[r - 1][c + 1] == piece and board[r - 2][c + 2] == piece and \
                    board[r - 3][
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
            window = row_array[c:c + WINDOW_LENGTH]
            score += evaluate_window(window, piece)

    # Score Vertical
    for c in range(COLUMN_COUNT):
        col_array = [int(i) for i in list(board[:, c])]
        for r in range(ROW_COUNT - 3):
            window = col_array[r:r + WINDOW_LENGTH]
            score += evaluate_window(window, piece)

    # Score posiive sloped diagonal
    for r in range(ROW_COUNT - 3):
        for c in range(COLUMN_COUNT - 3):
            window = [board[r + i][c + i] for i in range(WINDOW_LENGTH)]
            score += evaluate_window(window, piece)

    for r in range(ROW_COUNT - 3):
        for c in range(COLUMN_COUNT - 3):
            window = [board[r + 3 - i][c + i] for i in range(WINDOW_LENGTH)]
            score += evaluate_window(window, piece)

    return score

# this function checks the board if there is a winner
def endOfGame(board):
    return winningMove(board, PLAYER_PIECE) or winningMove(board, AI_PIECE) or len(validLocations(board)) == 0

# this function uses minimax to determan the next move to make
def minimax(board, depth, maximizingPlayer):
    valid_locations = validLocations(board)
    terminal = endOfGame(board)
    if depth == 0 or terminal:
        if terminal:
            if winningMove(board, AI_PIECE):
                return (None, 100000000000000)
            elif winningMove(board, PLAYER_PIECE):
                return (None, -10000000000000)
            else:
                return (None, 0)
        else:
            return (None, score(board, AI_PIECE))
    if maximizingPlayer:
        best_score = -math.inf
        column = random.choice(valid_locations)
        for col in valid_locations:
            row = nextOpenRow(board, col)
            b_copy = board.copy()
            placeAPiece(b_copy, row, col, AI_PIECE)
            new_score = minimax(b_copy, depth - 1, False)[1]
            if new_score > best_score:
                best_score = new_score
                column = col
        return column, best_score

    else:  # Minimizing player
        best_score = math.inf
        column = random.choice(valid_locations)
        for col in valid_locations:
            row = nextOpenRow(board, col)
            b_copy = board.copy()
            placeAPiece(b_copy, row, col, PLAYER_PIECE)
            new_score = minimax(b_copy, depth - 1, True)[1]
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
def player_move(board, col):
    # loc = validLocations(board)
    # loc.reverse()
    # print(loc)
    # get_input = int(input("choose your column: "))
    nextOpenRow(board, col)
    placeAPiece(board, nextOpenRow(board, col), col, PLAYER_PIECE)
    return True

# this fucntion uses a randomizer to determan the next move
def random_player(board):
    validLocations(board)
    col = random.choice(validLocations(board))
    row = nextOpenRow(board, col)
    placeAPiece(board, row, col, PLAYER_PIECE)

# this function actives the AI_player
def AI_player(board, level, piece):  # level gaat expoinenteel meer tijd kosten per level
    mini_max = minimax(board, level, True)
    col = mini_max[0]
    validLocations(board)
    row = nextOpenRow(board, col)
    placeAPiece(board, row, col, piece)
    return col

###################################################################
###########################__TKINTER__#############################
###################################################################

root = tk.Tk()
bot_frame = tk.Frame(root)
bot_frame.config(bg='#ffc32b')
myCanvas = tk.Canvas(root)
myCanvas.configure(height="670" , width="750", bg="#173cf2", highlightthickness=0, relief="raised", bd=5)
root.minsize(1300, 850)
board = create_board()

def create_circle(x, y, r, canvasName, color): #center coordinates, radius
    x0 = x - r
    y0 = y - r
    x1 = x + r
    y1 = y + r
    circle = canvasName.create_oval(x0, y0, x1, y1)
    return circle,myCanvas.itemconfig(circle, fil=color)

def place_col(x,y,size,color):
    amount = 0
    x += 10
    y += 10
    while amount != ROW_COUNT:
        placeholder = create_circle(x, y, size, myCanvas, color)
        amount += 1
        y = y + size * 2 + 5

def placeBoard(x,y,size):
    amount = 0
    x = 50
    y = 80
    while amount != COLUMN_COUNT:
        place_col(x, y, size, "#ededed")
        x = x + size * 2 + 5
        amount += 1

var = tk.IntVar()
def player_move_GUI(col):
    var.set(1)
    row = nextOpenRow(board,col)
    if row == None:
        row = 5
    drop_piece(col, row, "#ffc32b")
    player_move(board, col)

title = tk.Label(root, text="connect four", font=("Arial", 30),bg="#ededed", bd=5)
title.pack(fill="x")

c1 = tk.Button(root, text="1", width=12,height=2,relief="ridge", bg="#ffc32b", command=lambda j=6: player_move_GUI(j))
c1.pack(in_=bot_frame, side="left", padx=5, pady=2)
c2 = tk.Button(root, text="2",width=12,height=2,relief="ridge", bg="#ffc32b", command=lambda j=5: player_move_GUI(j))
c2.pack(in_=bot_frame, side="left", padx=5, pady=2)
c3 = tk.Button(root, text="3",width=12,height=2,relief="ridge", bg="#ffc32b", command=lambda j=4: player_move_GUI(j))
c3.pack(in_=bot_frame, side="left", padx=5, pady=2)
c4 = tk.Button(root, text="4",width=12,height=2,relief="ridge", bg="#ffc32b", command=lambda j=3: player_move_GUI(j))
c4.pack(in_=bot_frame, side="left", padx=5, pady=2)
c5 = tk.Button(root, text="5",width=12,height=2,relief="ridge", bg="#ffc32b", command=lambda j=2: player_move_GUI(j))
c5.pack(in_=bot_frame, side="left", padx=5, pady=2)
c6 = tk.Button(root, text="6",width=12,height=2,relief="ridge", bg="#ffc32b", command=lambda j=1: player_move_GUI(j))
c6.pack(in_=bot_frame, side="left", padx=5, pady=2)
c7 = tk.Button(root, text="7",width=12,height=2,relief="ridge", bg="#ffc32b", command=lambda j=0: player_move_GUI(j))
c7.pack(in_=bot_frame, side="left", padx=5, pady=2)

def connect_four_AI(turn):
    terminal = endOfGame(board)
    simple_draw_board(board)
    if terminal:
        new_window = tk.Toplevel(root)
        new_window.geometry("500x500")
        if winningMove(board, AI_PIECE):
            label = tk.Label(new_window, text="The AI won LMAO Loser!!", font=("Arial", 25))
            label.pack()
            print("Winner is AI!")
        elif winningMove(board, PLAYER_PIECE):
            label = tk.Label(new_window, text="You won against a AI wel done", font=("Arial", 25))
            label.pack()
            print("Winner is Player!")
        else:
            label = tk.Label(new_window, text="It is a Tie", font=("Arial", 25))
            label.pack()
            print("Tie!")
    if turn % 2 == 0:
        AI = AI_player(board, DEPTH_PLAYER_1, AI_PIECE)
        row = nextOpenRow(board, AI)
        if  row == None:
            row = 6
        drop_piece(AI , row -1, "#c70839")
        time.sleep(2)
    else:
        root.configure(bg="#ffc32b")
        bot_frame.pack()
        print("waiting")
        c1.wait_variable(var)
        print("stop waiting")
        bot_frame.pack_forget()
        root.configure(bg="#c70839")
    root.update()
    root.after(50, connect_four_AI(turn + 1))


def drop_piece(col,row, color):
    corrected_col  = 6 - col
    corrected_row = 5 - row
    x = 60
    y = 90
    for r in range(0,corrected_col):
        x = x + 50 * 2 + 5
    for c in range(0,corrected_row):
        y = y + 50 * 2 + 5
    piece = create_circle(x, y, 50, myCanvas, color)

placeBoard(0,0,50)
myCanvas.pack()
root.after(50, connect_four_AI(+1))
root.mainloop()