"""Console implementation of the 'Four in a Row' game."""
from typing import List, Tuple

ROWS = 6
COLUMNS = 7
EMPTY = " "
PLAYER_TOKENS = ("X", "O")


def create_board() -> List[List[str]]:
    """Create an empty game board."""
    return [[EMPTY for _ in range(COLUMNS)] for _ in range(ROWS)]


def print_board(board: List[List[str]]) -> None:
    """Print the current board to the console."""
    print()
    for row in board:
        print("|" + "|".join(cell or EMPTY for cell in row) + "|")
    print(" " + " ".join(str(i + 1) for i in range(COLUMNS)))
    print()


def drop_piece(board: List[List[str]], column: int, token: str) -> bool:
    """Drop a piece into the chosen column. Return True if successful."""
    if column < 0 or column >= COLUMNS:
        return False
    for row in range(ROWS - 1, -1, -1):
        if board[row][column] == EMPTY:
            board[row][column] = token
            return True
    return False


def check_direction(
    board: List[List[str]], start_row: int, start_col: int, delta_row: int, delta_col: int
) -> bool:
    """Check four in a row in one direction starting from given cell."""
    token = board[start_row][start_col]
    if token == EMPTY:
        return False
    for step in range(1, 4):
        r = start_row + step * delta_row
        c = start_col + step * delta_col
        if not (0 <= r < ROWS and 0 <= c < COLUMNS):
            return False
        if board[r][c] != token:
            return False
    return True


def has_winner(board: List[List[str]]) -> bool:
    """Return True if there is a winning line on the board."""
    directions: Tuple[Tuple[int, int], ...] = (
        (0, 1),   # horizontal
        (1, 0),   # vertical
        (1, 1),   # main diagonal
        (1, -1),  # anti diagonal
    )
    for row in range(ROWS):
        for col in range(COLUMNS):
            for d_row, d_col in directions:
                if check_direction(board, row, col, d_row, d_col):
                    return True
    return False


def is_draw(board: List[List[str]]) -> bool:
    """Return True if the board is full and there is no winner."""
    return all(board[0][col] != EMPTY for col in range(COLUMNS))


def ask_column(player_token: str) -> int:
    """Ask the player for a column number (1-based) and return zero-based index."""
    while True:
        choice = input(f"Player {player_token}, choose column (1-{COLUMNS}): ").strip()
        try:
            column = int(choice) - 1
            if 0 <= column < COLUMNS:
                return column
        except ValueError:
            # Non-integer input
            pass
        print(f"Invalid input. Enter a number from 1 to {COLUMNS}.")


def main() -> None:
    """Run console implementation of the 'Four in a Row' game."""
    board = create_board()
    current_player_index = 0

    while True:
        print_board(board)
        token = PLAYER_TOKENS[current_player_index]
        column = ask_column(token)

        if not drop_piece(board, column, token):
            print("This column is full. Choose another one.")
            continue

        if has_winner(board):
            print_board(board)
            print(f"Player {token} wins!")
            break

        if is_draw(board):
            print_board(board)
            print("It's a draw! No more moves possible.")
            break

        current_player_index = 1 - current_player_index


if __name__ == "__main__":
    main()
