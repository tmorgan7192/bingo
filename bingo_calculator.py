from enum import Enum
from math import factorial, perm, prod

bingo = ["B", "I", "N", "G", "O"]
ognib = ["O", "G", "N", "I", "B"]
starting_count = {'B': 0, 'I': 0, 'N': 1 , 'G': 0, 'O': 0}
stats = {}


class Outcome(Enum):
    NO_BINGO = 1
    MULTIPLE_BINGO = 2
    ROW_BINGO = 3
    COLUMN_BINGO = 4


def increment_ball_count(ball_count):
    for letter in ognib:
        if letter_on_board_count(ball_count, letter) == 5:
            if letter != 'B':
                ball_count[letter] = 0
                continue
            else:
                return True
        else:
            ball_count[letter] += 1
            return False


def check_bingo(ball_count):
    if is_multiple_bingo(ball_count):
        return False, Outcome.MULTIPLE_BINGO
    elif is_row_bingo(ball_count):
        return True, Outcome.ROW_BINGO
    elif is_col_bingo(ball_count):
        return True, Outcome.COLUMN_BINGO
    return False, Outcome.NO_BINGO


def is_multiple_bingo(ball_count):
    num_maxed_out_letters = len(maxed_out_letters(ball_count))
    return (
        num_maxed_out_letters > 1
        or {"B", "I", "G", "O"}.issubset(letters_with_min_count(ball_count, 2))
        or (
            num_maxed_out_letters == 1
            and {"B", "I", "G", "O"}.issubset(letters_with_min_count(ball_count, 1))
        )
    )


def is_row_bingo(ball_count):
    return letters_with_min_count(ball_count, 1) == bingo


def is_col_bingo(ball_count):
    return len(maxed_out_letters(ball_count)) == 1


def maxed_out_letters(ball_count):
    return [letter for letter in bingo if letter_on_board_count(ball_count, letter) == 5]


def letters_with_min_count(ball_count, min_count):
    return [letter for letter in bingo if letter_on_board_count(ball_count, letter) >= min_count]


def count_one_letters(ball_count):
    return list(
        set(letters_with_min_count(ball_count, 1))
        .difference(set(letters_with_min_count(ball_count, 2)).union({'N'}))
    )


def letter_on_board_count(ball_count, letter):
    return ball_count[letter] + starting_count[letter]


def get_combinations(ball_count, do_log, to_print):
    if do_log:
        for letter in bingo:
            to_print += str(ball_count[letter]) + "! * "
        to_print = to_print[0:len(to_print) - 2] + ") (number of re-orderings of same-lettered balls)\n"

    return prod([factorial(ball_count[letter]) for letter in bingo]), to_print


def score(ball_count, outcome, do_log = False, add_stats = False):
    if outcome in [Outcome.NO_BINGO, Outcome.MULTIPLE_BINGO]:
        return "Not Scored"
    num_balls = sum(ball_count.values())
    probability = 1 / perm(75, num_balls)
    numberings = prod([perm(15, ball_count[letter]) for letter in bingo])
    orderings = factorial(num_balls - 1) # -1 because the last draw must be last
    num_final_balls = num_balls
    if outcome == Outcome.ROW_BINGO:
          num_final_balls = len(count_one_letters(ball_count))
    if outcome == Outcome.COLUMN_BINGO:
          num_final_balls = 5 - starting_count[maxed_out_letters(ball_count)[0]]
    to_print = ""

    if do_log:
        to_print += "1 / (75 P " + str(num_balls) + ") (probability of specific game)\n"
        to_print += "   "
        for letter in bingo:
            to_print += " * (15 P " + str(ball_count[letter]) + ")"
        to_print += " (number of re-numberings)\n"
        to_print += "    * "
        to_print += "(" + str(num_balls) + " - 1)! (number of re-orderings fixing the last ball)\n"
        to_print += "    * "
        to_print += str(num_final_balls) + " (number of possible last balls)\n"
        to_print += "    / ( "

    combinations, to_print = get_combinations(ball_count, do_log, to_print)

    if do_log:
        print(to_print)

    stat = probability * numberings * orderings * num_final_balls / combinations

    if add_stats:
        stats[num_balls] = stat if num_balls not in stats.keys() else stats[num_balls] + stat

    return stat


def perform_calculation():
    ball_count = {'B': 0, 'I': 0, 'N': 0, 'G': 0, 'O': 0}
    exit_loop = increment_ball_count(ball_count)
    while not exit_loop:
        is_bingo, outcome = check_bingo(ball_count)
        score(ball_count, outcome, False, True)
        print(
            str(outcome)[8:len(str(outcome))] + ": " + str(ball_count)
            + ", Score: " + str(score(ball_count, outcome, False, False))
        )
        exit_loop = increment_ball_count(ball_count)

    print("\n\nExpected Value: " + str(sum([key * stats[key] for key in stats.keys()])))
    print("\nDistribution: ")
    print_stats(stats)


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
    print("3. All but the last ball can appear in any order.  Multiply by the number of re-orderings fixing the last ball")
    print("4. Multiply by the number of possible last balls")
    print("5. We double counted re-orderings among same-letter balls.  Divide this out")


def print_scoring_examples():
    print("\n\n----------- scoring examples ----------\n\n")
    examples = [
        {'B': 0, 'I': 2, 'N': 2, 'G': 0, 'O': 0},
        {'B': 2, 'I': 2, 'N': 0, 'G': 2, 'O': 2},
        {'B': 1, 'I': 1, 'N': 0, 'G': 1, 'O': 1},
        {'B': 1, 'I': 1, 'N': 0, 'G': 1, 'O': 2},
        {'B': 1, 'I': 1, 'N': 3, 'G': 2, 'O': 1},
        {'B': 0, 'I': 0, 'N': 4, 'G': 0, 'O': 0},
        {'B': 0, 'I': 0, 'N': 0, 'G': 5, 'O': 0},
        {'B': 3, 'I': 4, 'N': 3, 'G': 0, 'O': 5}
    ]
    for ball_count in examples:
        print("----------- example ----------\n")
        is_bingo, outcome = check_bingo(ball_count)
        print(
            str(outcome)[8:len(str(outcome))] + ": " + str(ball_count)
            + ", Score: " + str(score(ball_count, outcome, False, False))
        )
        print("")
        score(ball_count, outcome, True, False)


perform_calculation()
print_scoring_logic()
print_scoring_examples()