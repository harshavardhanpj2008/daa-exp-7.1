import os
from http.server import BaseHTTPRequestHandler, HTTPServer
from urllib.parse import urlparse, parse_qs


# -----------------------------
# Check whether queen is safe
# -----------------------------
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


# -----------------------------
# N-Queens Backtracking
# -----------------------------
def solve_n_queens(n):
    board = [-1] * n
    solutions = []
    backtrack_count = [0]

    def backtrack(row):
        # All queens placed
        if row == n:
            solutions.append(board[:])
            return

        for col in range(n):
            if is_safe(board, row, col):
                board[row] = col

                # Place queen in next row
                backtrack(row + 1)

                # Undo placement
                board[row] = -1
                backtrack_count[0] += 1

    backtrack(0)

    return solutions, backtrack_count[0]


# -----------------------------
# Create HTML chess board
# -----------------------------
def display_board(solution, n):
    html = '<table class="board">'

    for row in range(n):
        html += "<tr>"

        for col in range(n):
            if solution[row] == col:
                html += '<td class="queen">Q</td>'
            else:
                html += '<td>.</td>'

        html += "</tr>"

    html += "</table>"

    return html


# -----------------------------
# Generate Web Page
# -----------------------------
def generate_page():

    html = """
<!DOCTYPE html>
<html>
<head>

<title>N-Queens Problem - DAA</title>

<meta name="viewport" content="width=device-width, initial-scale=1">

<style>

* {
    box-sizing: border-box;
}

body {
    margin: 0;
    font-family: Arial, sans-serif;
    background: #f4f6f8;
    color: #222;
}

.header {
    background: #222;
    color: white;
    padding: 25px;
    text-align: center;
}

.container {
    max-width: 1100px;
    margin: 30px auto;
    padding: 20px;
}

.card {
    background: white;
    padding: 25px;
    margin-bottom: 25px;
    border-radius: 12px;
    box-shadow: 0 4px 15px rgba(0,0,0,0.08);
}

h1 {
    margin-bottom: 10px;
}

h2 {
    margin-top: 0;
}

.experiment {
    text-align: center;
}

.results {
    display: flex;
    justify-content: center;
    gap: 20px;
    flex-wrap: wrap;
}

.result-box {
    background: #f8f8f8;
    padding: 20px;
    border-radius: 10px;
    min-width: 220px;
}

.result-box h3 {
    margin-top: 0;
}

.value {
    font-size: 28px;
    font-weight: bold;
}

.solution {
    margin-top: 35px;
    text-align: center;
}

.board {
    border-collapse: collapse;
    margin: 15px auto;
}

.board td {
    width: 55px;
    height: 55px;
    border: 1px solid #333;
    text-align: center;
    font-size: 28px;
    font-weight: bold;
}

.board tr:nth-child(odd) td:nth-child(even),
.board tr:nth-child(even) td:nth-child(odd) {
    background: #ddd;
}

.board tr:nth-child(odd) td:nth-child(odd),
.board tr:nth-child(even) td:nth-child(even) {
    background: white;
}

.queen {
    font-size: 30px;
}

.info {
    line-height: 1.7;
}

.footer {
    text-align: center;
    padding: 20px;
    color: #666;
}

@media (max-width: 600px) {

    .board td {
        width: 40px;
        height: 40px;
        font-size: 22px;
    }

}

</style>

</head>

<body>

<div class="header">

<h1>N-Queens Problem</h1>

<p>Solving N-Queens using Backtracking</p>

<p>CS5303 - Design and Analysis of Algorithms Lab</p>

</div>

<div class="container">

<div class="card experiment">

<h2>Experiment Results</h2>

<p>
The program solves the N-Queens problem for N = 4, 6 and 8.
</p>

"""

    # -----------------------------
    # Solve N = 4, 6, 8
    # -----------------------------

    all_results = {}

    for n in [4, 6, 8]:

        solutions, backtracks = solve_n_queens(n)

        all_results[n] = (solutions, backtracks)

        html += f"""
<div class="card">

<h2>N = {n}</h2>

<div class="results">

<div class="result-box">

<h3>Solutions</h3>

<div class="value">
{len(solutions)}
</div>

</div>

<div class="result-box">

<h3>Backtracks</h3>

<div class="value">
{backtracks}
</div>

</div>

</div>

"""

        # Display all solutions for N = 4
        if n == 4:

            html += """
<h2 style="margin-top:30px;">
All Solutions for N = 4
</h2>
"""

            for i, solution in enumerate(solutions, 1):

                html += f"""

<div class="solution">

<h3>Solution {i}</h3>

<p>
Array Representation:
{solution}
</p>

{display_board(solution, n)}

</div>

"""

        else:

            html += """
<p>
Only the solution count is displayed for this value of N.
</p>
"""

        html += """
</div>
"""

    # -----------------------------
    # Algorithm information
    # -----------------------------

    html += """

<div class="card info">

<h2>Algorithm</h2>

<p>
The N-Queens problem places N queens on an N × N chessboard
such that no two queens attack each other.
</p>

<h3>Backtracking Approach</h3>

<ol>

<li>Start from the first row.</li>

<li>Try placing a queen in each column.</li>

<li>Check whether the position is safe.</li>

<li>If safe, move to the next row.</li>

<li>If no position is possible, backtrack to the previous row.</li>

<li>Continue until all queens are placed.</li>

</ol>

<h3>Safety Conditions</h3>

<ul>

<li>No two queens can be in the same column.</li>

<li>No two queens can be on the same diagonal.</li>

</ul>

<h3>Time Complexity</h3>

<p>
Approximately O(N!) in the worst case.
</p>

</div>

</div>

<div class="footer">

<p>N-Queens Problem | DAA Lab | Backtracking</p>

</div>

</body>

</html>
"""

    return html


# -----------------------------
# HTTP Server
# -----------------------------
class NQueensHandler(BaseHTTPRequestHandler):

    def do_GET(self):

        parsed_url = urlparse(self.path)

        if parsed_url.path != "/":
            self.send_error(404, "Page Not Found")
            return

        html = generate_page()

        self.send_response(200)

        self.send_header(
            "Content-Type",
            "text/html; charset=utf-8"
        )

        self.send_header(
            "Content-Length",
            str(len(html.encode("utf-8")))
        )

        self.end_headers()

        self.wfile.write(
            html.encode("utf-8")
        )


# -----------------------------
# Start Server
# -----------------------------
def main():

    # Render provides PORT automatically.
    # For local execution, port 10000 is used.
    port = int(
        os.environ.get("PORT", 10000)
    )

    server = HTTPServer(
        ("0.0.0.0", port),
        NQueensHandler
    )

    print(
        f"N-Queens server running on port {port}"
    )

    server.serve_forever()


if __name__ == "__main__":
    main()
