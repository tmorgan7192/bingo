import itertools
from random import choice as c
import statistics
import sys

num_boards = int(sys.argv[1])
trials = int(sys.argv[2])
check_number = int(sys.argv[3])
pull_stats = []


def mk_letter(col):
    if col == 0:
        return 'B'
    elif col == 1:
        return 'I'
    elif col == 2:
        return 'N'
    elif col == 3:
        return 'G'
    elif col == 4:
        return 'O'


def get_col(ball):
    if ball[0] == 'B':
        return 0
    elif ball[0] == 'I':
        return 1
    elif ball[0] == 'N':
        return 2
    elif ball[0] == 'G':
        return 3
    elif ball[0] == 'O':
        return 4
    return -1


def mk_number(number_list):
    number = c(number_list)
    number_list.remove(number)
    return number


def mk_bingo_board():
    lists = [list(range(1, 16)), list(range(16, 31)), list(range(31, 46)), list(range(46, 61)), list(range(61, 76))]

    board = [['X' for _ in range(5)] for _ in range(5)]
    for col in range(5):
        letter = mk_letter(col)

        for row in range(5):
            if not (col == 2 and row == 2):
                board[row][col] = letter + str(mk_number(lists[col]))

    return board


def mark_bingo_board(board, ball):
    col = get_col(ball)
    for row in range(5):
        if board[row][col] == ball:
            board[row][col] = 'X'
            # print_board(board)
            return row, col
    return -1, col


def pull_ball(balls):
    ball = c(balls)
    balls.remove(ball)
    return ball


def check_for_bingo(boards, ball):
    for board in boards:
        row, col = mark_bingo_board(board, ball)
        if row != -1 and (check_row(row, board) or check_col(col, board) or check_diagonals(board)):
            return True
    return False


def check_row(row, board):
    for col in range(5):
        if board[row][col] != 'X':
            return False
    return True


def check_col(col, board):
    for row in range(5):
        if board[row][col] != 'X':
            return False
    return True


def check_diagonals(board):
    for index in range(5):
        if board[index][index] != 'X':
            break
        if index == 4:
            return True
    for index in range(5):
        if board[index][4 - index] != 'X':
            break
        if index == 4:
            return True
    return False


def print_board(board):
    print("")
    for row in range(5):
        print(board[row])
    print("")


for n in range(trials):
    bingo_balls = [
        letter + str(number) for (letter, number)
        in list(itertools.product(['B'], list(range(1, 16))))
        + list(itertools.product(['I'], list(range(16, 31))))
        + list(itertools.product(['N'], list(range(31, 46))))
        + list(itertools.product(['G'], list(range(46, 61))))
        + list(itertools.product(['O'], list(range(61, 76))))
    ]
    bingo_boards = [mk_bingo_board() for _ in range(num_boards)]
    new_ball = pull_ball(bingo_balls)
    num_pulls = 1

    while not check_for_bingo(bingo_boards, new_ball):
        new_ball = pull_ball(bingo_balls)
        num_pulls += 1

    pull_stats.append(num_pulls)
    if (n + 1) % check_number == 0:
        print("Trials: " + str(n + 1) + ", Average number of pulls: " + str(statistics.mean(pull_stats)))
