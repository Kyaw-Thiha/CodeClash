#!/usr/bin/env python3
"""
Code Clash Tic Tac Toe Bot Challenge — Python Starter Bot

Welcome to the Code Clash Tic Tac Toe Bot Competition! This is your starter template.
Modify any part of this file to implement your own strategy.

-------------------------------------------
How to package your bot as a single file:
-------------------------------------------
1. Install PyInstaller:
   pip install pyinstaller

2. Build a one-file executable:
   pyinstaller --onefile starter_bot.py

3. Your executable lives in dist/ (e.g., dist/starter_bot.exe)

For rules, move format, and submission details see design_doc.md.
"""

import sys
import json

def get_valid_moves(board):
    """Return list of empty ([row, col]) cells on the board."""
    moves = []
    for i in range(len(board)):
        for j in range(len(board[i])):
            if board[i][j] == "":
                moves.append((i, j))
    return moves

def choose_move(board, player):
    """
    TODO: Implement your move selection logic.
    Should return a tuple (row, col) from get_valid_moves(board).
    """
    valid = get_valid_moves(board)
    if not valid:
        raise Exception("No valid moves available")
    # Example stub: always pick the first one
    return valid[0]

def main():
    if len(sys.argv) != 2:
        print("Usage: python starter_bot.py <state.json>", file=sys.stderr)
        sys.exit(1)

    # 1) Load state.json
    try:
        with open(sys.argv[1], 'r', encoding='utf-8') as f:
            data = json.load(f)
            board = data['board']
            player = data['player']
    except Exception as e:
        print(f"ERROR: Failed to load input: {e}", file=sys.stderr)
        sys.exit(1)

    # 2) Choose move
    try:
        row, col = choose_move(board, player)
    except Exception as e:
        print(f"ERROR: {e}", file=sys.stderr)
        sys.exit(1)

    # 3) Output result
    print(json.dumps([row, col]))
    sys.exit(0)

if __name__ == '__main__':
    main()