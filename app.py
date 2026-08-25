from flask import Flask, render_template_string

app = Flask(__name__)


def is_safe(board, row, col):
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
    board = [-1] * n
    solutions = []
    backtrack_count = [0]

    def backtrack(row):
        if row == n:
            solutions.append(board[:])
            return

        for col in range(n):
            if is_safe(board, row, col):
                board[row] = col

                backtrack(row + 1)

                # Undo
                board[row] = -1
                backtrack_count[0] += 1

    backtrack(0)

    return solutions, backtrack_count[0]


HTML = """
<!DOCTYPE html>
<html>
<head>
    <title>N-Queens Solver</title>
    <style>
        body {
            font-family: Arial, sans-serif;
            background: #f4f4f4;
            text-align: center;
            padding: 30px;
        }

        h1 {
            color: #222;
        }

        .container {
            background: white;
            max-width: 900px;
            margin: auto;
            padding: 30px;
            border-radius: 12px;
            box-shadow: 0 4px 15px rgba(0,0,0,0.1);
        }

        input {
            padding: 10px;
            width: 100px;
            font-size: 16px;
        }

        button {
            padding: 10px 20px;
            font-size: 16px;
            cursor: pointer;
            background: #222;
            color: white;
            border: none;
            border-radius: 6px;
        }

        .result {
            margin-top: 25px;
        }

        .board {
            margin: 20px auto;
            border-collapse: collapse;
        }

        .board td {
            width: 45px;
            height: 45px;
            border: 1px solid #333;
            text-align: center;
            font-size: 28px;
        }

        .board tr:nth-child(even) td:nth-child(odd),
        .board tr:nth-child(odd) td:nth-child(even) {
            background: #ddd;
        }

        .board tr:nth-child(even) td:nth-child(even),
        .board tr:nth-child(odd) td:nth-child(odd) {
            background: #fff;
        }

        .solution {
            margin: 30px 0;
        }
    </style>
</head>

<body>

<div class="container">

    <h1>♛ N-Queens Solver</h1>

    <form method="GET">
        <input
            type="number"
            name="n"
            value="{{ n }}"
            min="1"
            max="12"
            required
        >

        <button type="submit">Solve</button>
    </form>

    {% if solved %}

        <div class="result">

            <h2>N = {{ n }}</h2>

            <p>
                <strong>{{ solution_count }}</strong>
                solutions found
            </p>

            <p>
                Backtracking operations:
                <strong>{{ backtracks }}</strong>
            </p>

            {% if n <= 6 %}

                <h2>Solutions</h2>

                {% for solution in solutions %}

                    <div class="solution">

                        <h3>Solution {{ loop.index }}</h3>

                        <table class="board">

                            {% for row in range(n) %}

                                <tr>

                                    {% for col in range(n) %}

                                        <td>
                                            {% if solution[row] == col %}
                                                ♛
                                            {% else %}
                                                .
                                            {% endif %}
                                        </td>

                                    {% endfor %}

                                </tr>

                            {% endfor %}

                        </table>

                    </div>

                {% endfor %}

            {% else %}

                <p>
                    Board display is hidden for N > 6
                    to avoid displaying too many solutions.
                </p>

            {% endif %}

        </div>

    {% endif %}

</div>

</body>
</html>
"""


@app.route("/")
def home():
    n = int(request.args.get("n", 4)) if request.args.get("n") else 4

    if n < 1:
        n = 1

    if n > 12:
        n = 12

    solutions, backtracks = solve_n_queens(n)

    # Display solutions only for smaller boards
    display_solutions = solutions if n <= 6 else []

    return render_template_string(
        HTML,
        n=n,
        solved=True,
        solutions=display_solutions,
        solution_count=len(solutions),
        backtracks=backtracks
    )


if __name__ == "__main__":
    app.run()
