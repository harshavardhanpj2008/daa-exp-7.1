def is_safe(board, row, col):
    """
    Check whether placing a queen at (row, col) is safe.
    """
    for prev_row in range(row):
        placed = board[prev_row]

        # Same column
        if placed == col:
            return False

        # Same diagonal
        if abs(prev_row - row) == abs(placed - col):
            return False

    return True


def solve_n_queens(n):
    """
    Solve the N-Queens problem using backtracking.

    Returns:
        solutions: List of all valid solutions
        backtrack_count: Number of backtracking operations
    """
    board = [-1] * n
    solutions = []
    backtrack_count = [0]

    def backtrack(row):
        # All queens have been placed
        if row == n:
            solutions.append(board[:])
            return

        for col in range(n):
            if is_safe(board, row, col):
                board[row] = col

                # Place queen in next row
                backtrack(row + 1)

                # Undo the placement
                board[row] = -1
                backtrack_count[0] += 1

    backtrack(0)

    return solutions, backtrack_count[0]


def display_board(solution, n):
    """
    Display an N-Queens solution as a chess board.
    """
    print("+" + "---+" * n)

    for row in range(n):
        print("|", end="")

        for col in range(n):
            if solution[row] == col:
                print(" Q |", end="")
            else:
                print(" . |", end="")

        print()
        print("+" + "---+" * n)


def main():
    # Solve for N = 4, 6 and 8
    for n in [4, 6, 8]:
        solutions, backtracks = solve_n_queens(n)

        print(f"\nN={n}: {len(solutions)} solutions, {backtracks} backtracks")

        # Display all solutions only for N=4
        if n == 4:
            print(f"\nAll solutions for {n}-Queens:")

            for i, solution in enumerate(solutions, 1):
                print(f"\nSolution {i}: {solution}")
                display_board(solution, n)


if __name__ == "__main__":
    main()
