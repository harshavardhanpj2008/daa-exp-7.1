# N-Queens Problem Using Backtracking

## DAA Lab - Experiment No. 7

This project solves the N-Queens problem using the Backtracking technique.

## Problem Statement

Place N queens on an N × N chessboard such that no two queens attack each other.

Two queens cannot be placed:

- In the same column
- On the same diagonal

## Algorithm

1. Start from the first row.
2. Try placing a queen in every column.
3. Check whether the position is safe.
4. If the position is safe, place the queen.
5. Move to the next row.
6. If no valid position is found, backtrack.
7. Continue until all queens are placed.
8. Store every valid solution.

## Technologies Used

- Python
- Python Standard Library
- HTTP Server
- Backtracking Algorithm

## Files

```text
app.py
requirements.txt
README.md
