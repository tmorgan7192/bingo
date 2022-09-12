from enum import Enum
from math import factorial, perm, prod

bingo = ["B", "I", "N", "G", "O"]
bigo = ['B', 'I', 'G', 'O']
ognib = ["O", "G", "N", "I", "B"]
max_balls_on_board = 5
max_balls_off_board = 10
starting_count = {'B': 0, 'I': 0, 'N': 1, 'G': 0, 'O': 0}
stats = {}


class Outcome(Enum):
    NO_BINGO = 1
    MULTIPLE_BINGO = 2
    ROW_BINGO = 3
    COLUMN_BINGO = 4


def increment_ball_count(balls_on_board, balls_off_board, outcome_is_bingo, print_balls_off_board):
    if balls_off_board != {'B': 10, 'I': 10, 'N': 11, 'G': 10, 'O': 10} and outcome_is_bingo:
        do_increment_ball_count(balls_off_board, max_balls_off_board)
        outcome = get_outcome(balls_on_board)
        score(balls_on_board, balls_off_board, outcome, False, True, print_balls_off_board, print_balls_off_board)
        return False
    else:
        reset_balls_off_board(balls_off_board)
        do_increment_ball_count(balls_on_board, max_balls_on_board)
        outcome = get_outcome(balls_on_board)
        while not is_bingo(outcome):
            do_increment_ball_count(balls_on_board, max_balls_on_board)
            outcome = get_outcome(balls_on_board)

        if balls_on_board['B'] == max_balls_on_board:
            return True
        score(balls_on_board, balls_off_board, outcome, False, True, True, print_balls_off_board)
        return False


def is_bingo(outcome):
    return outcome in [Outcome.COLUMN_BINGO, Outcome.ROW_BINGO]


def reset_balls_off_board(balls_off_board):
    for letter in bingo:
        balls_off_board[letter] = 0


def do_increment_ball_count(ball_count, max_count):
    for letter in ognib:
        if adjusted_letter_count(ball_count, letter, 1 if max_count == max_balls_on_board else -1) == max_count:
            if letter != 'B':
                ball_count[letter] = 0
                continue
            else:
                return True
        else:
            ball_count[letter] += 1
            skip_if_not_ascending(ball_count)
            return False


def skip_if_not_ascending(ball_count):
    max_letter = first_max_letter(ball_count)
    if max_letter != 'O' and ball_count[max_letter] != 0:
        for letter in ['O', 'G', 'I', 'B']:
            if letter != max_letter:
                ball_count[letter] = ball_count[max_letter]
            else:
                break


def first_max_letter(ball_count):
    return [letter for letter in bigo if ball_count[letter] == max([ball_count[key] for key in bigo])][0]


def get_outcome(balls_on_board):
    if is_multiple_bingo(balls_on_board):
        return Outcome.MULTIPLE_BINGO
    elif is_row_bingo(balls_on_board):
        return Outcome.ROW_BINGO
    elif is_col_bingo(balls_on_board):
        return Outcome.COLUMN_BINGO
    return Outcome.NO_BINGO


def is_multiple_bingo(balls_on_board):
    num_maxed_out_letters = len(maxed_out_letters(balls_on_board))
    return (
            num_maxed_out_letters > 1
            or {"B", "I", "G", "O"}.issubset(letters_with_min_count(balls_on_board, 2))
            or (
                    num_maxed_out_letters == 1
                    and {"B", "I", "G", "O"}.issubset(letters_with_min_count(balls_on_board, 1))
            )
    )


def is_row_bingo(balls_on_board):
    return letters_with_min_count(balls_on_board, 1) == bingo


def is_col_bingo(balls_on_board):
    return len(maxed_out_letters(balls_on_board)) == 1


def maxed_out_letters(balls_on_board):
    return [letter for letter in bingo if adjusted_letter_count(balls_on_board, letter) == max_balls_on_board]


def letters_with_min_count(balls_on_board, min_count):
    return [letter for letter in bingo if adjusted_letter_count(balls_on_board, letter) >= min_count]


def count_one_letters(balls_on_board):
    return list(
        set(letters_with_min_count(balls_on_board, 1))
            .difference(set(letters_with_min_count(balls_on_board, 2)).union({'N'}))
    )


def adjusted_letter_count(ball_count, letter, is_on_board=1):
    return ball_count[letter] + (starting_count[letter] * is_on_board)


def score(
    balls_on_board,
    balls_off_board,
    outcome,
    do_log=False,
    add_stats=False,
    print_score=True,
    print_balls_off_board=False
):
    if outcome in [Outcome.NO_BINGO, Outcome.MULTIPLE_BINGO]:
        do_print_score(outcome, balls_on_board, balls_off_board, "not scored", print_balls_off_board)
        if do_log:
            print("")
        return
    num_balls_on_board = sum(balls_on_board.values())
    num_balls_off_board = sum(balls_off_board.values())
    num_balls = num_balls_on_board + num_balls_off_board
    probability = 1 / perm(75, num_balls)
    numberings = (
        prod([perm(max_balls_on_board, balls_on_board[letter]) for letter in bingo]) *
        prod([perm(max_balls_off_board, balls_off_board[letter]) for letter in bingo])
    )
    orderings = factorial(num_balls - 1)
    num_final_balls = num_balls_on_board
    if outcome == Outcome.ROW_BINGO:
        num_final_balls = len(count_one_letters(balls_on_board))
    if outcome == Outcome.COLUMN_BINGO:
        num_final_balls = 5 - starting_count[maxed_out_letters(balls_on_board)[0]]
    to_print = ""

    if do_log:
        to_print += "1 / (75 P " + str(num_balls) + ") (probability of specific game)\n"
        to_print += "   "
        for letter in bingo:
            to_print += " * (" + str(max_balls_on_board) + " P " + str(balls_on_board[letter]) + ")"
        for letter in bingo:
            to_print += " * (" + str(max_balls_off_board) + " P " + str(balls_off_board[letter]) + ")"
        to_print += " (number of re-numberings)\n"
        to_print += "    * "
        to_print += "(" + str(num_balls) + " - 1)! (number of re-orderings fixing the last ball drawn)\n"
        to_print += "    * "
        to_print += str(num_final_balls) + " (number of possible last balls)\n"
        to_print += "    * "

    letter_perms_on_board, to_print = get_letter_perms(balls_on_board, do_log, to_print)
    if do_log:
        to_print += "on board)\n    * "
    letter_perms_off_board, to_print = get_letter_perms(balls_off_board, do_log, to_print)
    
    if do_log:
        to_print += "off board)\n     / ( "

    combinations, to_print = get_combinations(balls_on_board, balls_off_board, do_log, to_print)

    stat = (
        probability * numberings * orderings * num_final_balls * letter_perms_on_board * letter_perms_off_board
        / combinations
    )

    if add_stats:
        stats[num_balls] = stat if num_balls not in stats.keys() else stats[num_balls] + stat

    if print_score:
        do_print_score(outcome, balls_on_board, balls_off_board, stat, print_balls_off_board)
    if do_log:
        print("\n" + to_print)

    return stat


def get_combinations(balls_on_board, balls_off_board, do_log, to_print):
    if do_log:
        for letter in bingo:
            to_print += str(balls_on_board[letter]) + "! * "
        for letter in bingo:
            to_print += str(balls_off_board[letter]) + "! * "
        to_print = to_print[0:len(to_print) - 2] + ") (number of re-orderings of same-lettered balls)\n"

    return (
        prod([factorial(balls_on_board[letter]) for letter in bingo])
        * prod([factorial(balls_off_board[letter]) for letter in bingo])
        , to_print
    )


def get_letter_perms(ball_count, do_log, to_print):
    counts = {
        value: sum([1 for key in bigo if ball_count[key] == value])
        for value in [ball_count[letter] for letter in bigo]
    }
    total_count = sum(counts.values())
    if do_log and total_count > 0:
        to_print += str(total_count) + "! / "
        if len(counts.values()) > 1:
            to_print += "( "
        for count in counts.values():
            to_print += str(count) + "! * "
        to_print = to_print[0:len(to_print) - 2]
        if len(counts.values()) > 1:
            to_print += ") "
        to_print += "(number of letter permutations "

    return factorial(total_count) / prod([factorial(count) for count in counts.values()]), to_print


def perform_calculation(print_balls_off_board):
    balls_on_board = {'B': 0, 'I': 0, 'N': 0, 'G': 0, 'O': 1}
    balls_off_board = {'B': 0, 'I': 0, 'N': 0, 'G': 0, 'O': 0}

    exit_loop = False
    outcome = get_outcome(balls_on_board)
    while not is_bingo(outcome):
        increment_ball_count(balls_on_board, balls_off_board, is_bingo(outcome), print_balls_off_board)
        outcome = get_outcome(balls_on_board)
    while not exit_loop:
        exit_loop = increment_ball_count(balls_on_board, balls_off_board, is_bingo(outcome), print_balls_off_board)
        outcome = get_outcome(balls_on_board)

    print("\n\nExpected Value: " + str(sum([key * stats[key] for key in stats.keys()])))
    print("\nDistribution: ")
    print_stats(stats)


def do_print_score(outcome, balls_on_board, balls_off_board, score_to_print, print_balls_off_board):
    to_print = str(outcome)[8:len(str(outcome))] + " - Balls on board: " + str(balls_on_board)
    if print_balls_off_board:
        to_print += ", Balls off board: " + str(balls_off_board)
        to_print += ", Score: " + str(score_to_print)
    print(to_print)


def print_stats(stats_to_print):
    keys = list(stats_to_print.keys())
    keys.sort()
    for key in keys:
        if key < 10:
            print(str(key) + ":  " + str(stats_to_print[key]))
        else:
            print(str(key) + ": " + str(stats_to_print[key]))

    print("-------------------------")
    print("    " + str(sum(stats_to_print.values())))


def print_scoring_logic():
    print("\n\n----------- scoring logic ----------\n\n")
    print("1. Start with the probability of some specific bingo game matching the letter counts occurring")
    print("2. Multiply by the number of re-numberings of the balls")
    print("3. All but the last ball can appear in any order.  Multiply by the number of re-orderings fixing the last "
          "ball")
    print("4. Multiply by the number of possible last balls")
    print("5. The letters B, I, G, and O play equivalent rows in this scenario.  As such, we only score ball counts "
          "where these letter counts appear in increasing order.  Multiply by the number of re-orderings of these "
          "counts to account for this")
    print("6. We double counted re-orderings among same-letter balls.  Divide this out")


def print_scoring_examples():
    print("\n\n----------- scoring examples ----------\n\n")
    examples = [
        [{'B': 0, 'I': 0, 'N': 2, 'G': 0, 'O': 2}, {'B': 0, 'I': 0, 'N': 0, 'G': 0, 'O': 0}],
        [{'B': 2, 'I': 2, 'N': 0, 'G': 2, 'O': 2}, {'B': 2, 'I': 7, 'N': 6, 'G': 5, 'O': 8}],
        [{'B': 1, 'I': 1, 'N': 0, 'G': 1, 'O': 1}, {'B': 0, 'I': 0, 'N': 0, 'G': 0, 'O': 0}],
        [{'B': 1, 'I': 1, 'N': 0, 'G': 1, 'O': 2}, {'B': 1, 'I': 0, 'N': 2, 'G': 3, 'O': 4}],
        [{'B': 1, 'I': 1, 'N': 3, 'G': 1, 'O': 2}, {'B': 6, 'I': 4, 'N': 3, 'G': 9, 'O': 0}],
        [{'B': 0, 'I': 0, 'N': 4, 'G': 0, 'O': 0}, {'B': 0, 'I': 0, 'N': 0, 'G': 0, 'O': 0}],
        [{'B': 0, 'I': 0, 'N': 0, 'G': 0, 'O': 5}, {'B': 0, 'I': 0, 'N': 0, 'G': 0, 'O': 0}],
        [{'B': 1, 'I': 1, 'N': 1, 'G': 1, 'O': 1}, {'B': 0, 'I': 0, 'N': 0, 'G': 0, 'O': 0}],
        [{'B': 3, 'I': 4, 'N': 3, 'G': 0, 'O': 5}, {'B': 1, 'I': 2, 'N': 3, 'G': 4, 'O': 5}]
    ]

    for ball_count in examples:
        print("----------- example ----------\n")
        outcome = get_outcome(ball_count[0])
        score(ball_count[0], ball_count[1], outcome, True, False, True, True)


perform_calculation(False)
print_scoring_logic()
print_scoring_examples()
