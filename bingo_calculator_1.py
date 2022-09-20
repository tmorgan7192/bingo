from copy import deepcopy
from math import comb, floor


env_vars = {"PRINT_COUNT": 1000}


def o(f, g):
    return lambda x: f(g(x))


def get_row(n):
    return floor(n / 5)


def get_col(n):
    return n % 5


def identity(n):
    return n


def reflect(n):
    return get_index(get_row(n), 4 - get_col(n))


def rotate(n):
    def do_rotate(k):
        return get_index(get_col(k), 4 - get_row(k))
    if n == 1:
        return do_rotate
    else:
        return rotate(n - 1)


def swap_rows(row_1, row_2):
    def do_swap_rows(n):
        col = get_col(n)
        if get_row(n) == row_1:
            return get_index(row_2, col)
        elif get_row(n) == row_2:
            return get_index(row_1, col)
        else:
            return n
    return do_swap_rows


def swap_cols(col_1, col_2):
    def do_swap_cols(n):
        row = get_row(n)
        if get_col(n) == col_1:
            return get_index(row, col_2)
        elif get_col(n) == col_2:
            return get_index(row, col_1)
        else:
            return n
    return do_swap_cols


def get_index(row, col):
    return row * 5 + col


def equals(g, h):
    return all([g(n) == h(n) for n in range(25)])


def generate_group(generators):
    group = []
    new_group = deepcopy(generators)
    while len(group) != len(new_group):
        group = deepcopy(new_group)
        for generator in generators:
            for element in group:
                new_element = o(generator, element)
                if any([equals(new_element, test_element) for test_element in new_group]):
                    continue
                new_group.append(new_element)
    return new_group


square_symmetries = [
    rotate(1),
    rotate(2),
    rotate(3),
    reflect,
    o(reflect, rotate(1)),
    o(reflect, rotate(2)),
    o(reflect, rotate(3)),
]
row_swaps = [swap_rows(n, m) for m in range(1, 5) for n in range(m)]
col_swaps = [swap_cols(n, m) for m in range(1, 5) for n in range(m)]
rotate_row_swaps = [o(rotate(1), f) for f in row_swaps]
rotate_col_swaps = [o(rotate(1), f) for f in col_swaps]
function_pool = square_symmetries + row_swaps + col_swaps + rotate_row_swaps + rotate_col_swaps


bingos = [
    [0, 5, 10, 15, 20],
    [0, 6, 12, 18, 24]
]


def get_card(subset):
    bingo_card = [
        [1, 16, 31, 46, 61],
        [2, 17, 32, 47, 62],
        [3, 18, 'X', 48, 63],
        [4, 19, 34, 49, 64],
        [5, 20, 35, 50, 65]
    ]
    for n in range(25):
        is_marked = subset[n]
        row = get_row(n)
        col = get_col(n)
        if is_marked == 1:
            bingo_card[row][col] = 'X'

    return bingo_card


def count_bingos(card):
    return {
        "ROW_BINGO_COUNT": check_rows(card),
        "COL_BINGO_COUNT": check_cols(card),
        "DIAGONAL_BINGO_COUNT": check_diagonals(card)
    }


def card_has_bingo(outcome):
    return max(outcome.values()) > 0


def is_overshoot(outcome):
    return max(outcome.values()) > 1


def is_valid_ending_position(outcome):
    return card_has_bingo(outcome) and not is_overshoot(outcome)


def check_rows(card):
    row_bingo_count = 0
    for row in range(5):
        for col in range(5):
            if card[row][col] != 'X':
                break
            if col == 4:
                row_bingo_count += 1
    return row_bingo_count


def check_cols(card):
    col_bingo_count = 0
    for col in range(5):
        for row in range(5):
            if card[row][col] != 'X':
                break
            if row == 4:
                col_bingo_count += 1
    return col_bingo_count


def check_diagonals(card):
    diagonal_bingo_count = 0
    for i in range(5):
        if card[i][i] != 'X':
            break
        if i == 4:
            diagonal_bingo_count += 1
    for i in range(5):
        if card[i][4 - i] != 'X':
            break
        if i == 4:
            diagonal_bingo_count += 1
    return diagonal_bingo_count


def score_card(card, outcome, num_copies):
    balls_on_board = sum(col.count('X') for col in card) - 1
    print(f"BINGO! * {num_copies} (Balls on board: {balls_on_board}): {card}")
    print_card(card)
    score = 0
    for balls_off_board in range(52):
        num_balls = balls_on_board + balls_off_board
        score += num_balls / comb(75, num_balls - 1)
    return score * num_copies


def apply(f, subset):
    return {f(s): subset[s] for s in subset.keys()}


def swap_row_col_bingos(outcome):
    return {
        "ROW_BINGO_COUNT": outcome["COL_BINGO_COUNT"],
        "COL_BINGO_COUNT": outcome["ROW_BINGO_COUNT"],
        "DIAGONAL_BINGO_COUNT": outcome["DIAGONAL_BINGO_COUNT"]
    }


def visit_node(subset, visited):
    bingo_card = get_card(subset)
    outcome = count_bingos(bingo_card)
    if is_overshoot(outcome):
        visited[get_num_from_subset(subset)] = False
        return 0
    elif is_valid_ending_position(outcome):
        num_copies = 1
        for f in function_pool:
            new_subset = apply(f, subset)
            new_outcome = count_bingos(get_card(new_subset))
            if (
                new_subset != subset
                and not visited[get_num_from_subset(new_subset)]
                and (new_outcome == outcome or new_outcome == swap_row_col_bingos(outcome))
            ):
                visited[get_num_from_subset(new_subset)] = True
                num_copies += 1
        bingo_card = get_card(subset)
        return score_card(bingo_card, outcome, num_copies)
    else:
        return 0


def get_marked_nodes(subset):
    return [key for key in subset.keys() if subset[key] == 1]


def get_subset(marked_nodes):
    return {key: 1 if key in marked_nodes else 0 for key in range(25)}


def get_num_from_subset(subset):
    return sum([pow(2, key) for key in get_marked_nodes(subset)])


def get_neighbor(subset, n):
    return {key: subset[key] if key != n else 1 for key in subset.keys()}


def print_card(card):
    print("")
    for row in range(len(card)):
        print_row(card[row])
    print("")


def print_row(row):
    to_print = ""
    for i in range(len(row)):
        entry = str(row[i])
        to_print += entry
        to_print += " " * (3 - len(entry))
    to_print += "\n"
    print(to_print)


def main():
    run_tests()
    score = 0
    queue = [get_subset(bingo) for bingo in bingos]
    visited = {n: False for n in range(pow(2, 25))}
    print("Initialization complete")
    for bingo in queue:
        score += visit_node(bingo, visited)

    exit_loop = False
    while not exit_loop:
        node = queue.pop(0)
        if visited[get_num_from_subset(node)]:
            continue
        for n in range(25):
            if n != 12 and node[n] != 1:
                neighbor = get_neighbor(node, n)
                if len(get_marked_nodes(neighbor)) >= 17:
                    exit_loop = True
                    break
                if not visited[get_num_from_subset(neighbor)]:
                    queue.append(neighbor)
                    score += visit_node(neighbor, visited)
    print(f"Expected value: {score}")


def run_tests():
    test_square_symmetries()
    test_row_swaps()
    test_col_swaps()
    test_rotate_row_swaps()
    test_rotate_col_swaps()


def test_square_symmetries():
    assert len(square_symmetries) == 7
    for f in square_symmetries:
        n = [f(i) for i in range(25)]
        assert set(n) == set(range(25))
    print("Tested square symmetries")


def test_row_swaps():
    assert len(row_swaps) == 10
    for f in row_swaps:
        transformed_row = [f(i) for i in range(25)]
        assert set(transformed_row) == set(range(25))
    print("Tested row swaps")


def test_col_swaps():
    assert len(col_swaps) == 10
    for f in col_swaps:
        transformed_col = [f(i) for i in range(25)]
        assert set(transformed_col) == set(range(25))
    print("Tested col swaps")


def test_rotate_row_swaps():
    assert len(rotate_row_swaps) == 10
    for f in rotate_row_swaps:
        transformed_row = [f(i) for i in range(25)]
        assert set(transformed_row) == set(range(25))
    print("Tested rotate row swaps")


def test_rotate_col_swaps():
    assert len(rotate_col_swaps) == 10
    for f in rotate_col_swaps:
        transformed_col = [f(i) for i in range(25)]
        assert set(transformed_col) == set(range(25))
    print("Tested rotate col swaps")


if __name__ == "__main__":
    main()
