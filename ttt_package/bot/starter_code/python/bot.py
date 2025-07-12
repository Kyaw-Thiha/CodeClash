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


# Simon added libraries
from typing import List

# Simon added constants
SIZE = 10

def get_valid_moves(board):
    """Return list of empty ([row, col]) cells on the board."""
    moves = []
    for i in range(len(board)):
        for j in range(len(board[i])):
            if board[i][j] == "":
                moves.append((i, j))
    return moves


# ____________________Simon defined classes____________________
class Position:
    # Simon's datatype Line
    # Has attributes 
    #   x: int
    #   y: int
    # Attributes indicate the position of the piece
    def __init__(self, x: int, y: int):
        self.x = x
        self.y = y

    def __repr__(self) -> str:
        return f"Position({self.x}, {self.y})"


class Line:
    # Simon's datatype Line
    # Has attributes 
    #   num_pieces: int
    #   sides_blocked: int (0 or 1 or 2)
    #   positions: list[tuple[int,int]] (the positions of pieces on the line)
    def __init__(self, num_pieces: int, sides_blocked: int, positions: List[Position]):
        if len(positions) != num_pieces:
            raise ValueError("positions list must match num_pieces")
        self.num_pieces = num_pieces
        self.sides_blocked = sides_blocked
        self.positions = positions


    def __repr__(self) -> str:
        return f"Line(num_pieces={self.num_pieces}, sides_blocked={self.sides_blocked}, positions={self.positions})"

# ____________________Simon defined functions for getting all lines____________________


def getLineH(piece: Position, board: List[List[str]]) -> Line:
    # Simon's function
    # Takes a piece's position, and returns a line representing
    # the line from the current piece to the right until the 
    # piece is no longer of the same type or is empty
    #
    # The function returns an empty Line if the piece is not the
    # leftmost piece OR the piece is standalone to the right.

    # if current piece is not the leftmost piece, return empty line
    current = board[piece.y][piece.x]
    if(piece.x != 0 and board[piece.y][piece.x - 1] == current):
        return Line(0, 0, [])

    positions = [piece]
    sides_blocked = 0
    count = 1

    while(piece.x + count < SIZE and board[piece.y][piece.x + count] == current):
        positions.append(Position(piece.x + count, piece.y))
        count += 1

    if(piece.x == 0 or board[piece.y][piece.x - 1] != ''):
        sides_blocked += 1
    if(piece.x + count >= SIZE - 1 or board[piece.y][piece.x + count + 1] != ''):
        sides_blocked += 1

    return Line(len(positions), sides_blocked, positions)

def getLineV(piece: Position, board: List[List[str]]) -> Line:
    # Simon's function
    # Same as getLineH except it works for vertical line instead
    current = board[piece.y][piece.x]
    if(piece.y != 0 and board[piece.y - 1][piece.x] == current):
        return Line(0, 0, [])


    positions = [piece]
    sides_blocked = 0
    count = 1
    while(piece.y + count < SIZE and board[piece.y + count][piece.x] == current):
        positions.append(Position(piece.x, piece.y + count))
        count += 1

    if(piece.y == 0 or board[piece.y - 1][piece.x] != ''):
        sides_blocked += 1
    if(piece.y + count >= SIZE - 1 or board[piece.y + count + 1][piece.x] != ''):
        sides_blocked += 1

    return Line(len(positions), sides_blocked, positions)

def getLineD1(piece: Position, board: List[List[str]]) -> Line:
    # Simon's function
    # Same as getLineH except it works for diagonal line top left to bottom right
    current = board[piece.y][piece.x]
    if(piece.x != 0 and piece.y != 0 and board[piece.y - 1][piece.x - 1] == current):
        return Line(0, 0, [])

    positions = [piece]
    sides_blocked = 0
    count = 1
    while(piece.x + count < SIZE and piece.y + count < SIZE and board[piece.y + count][piece.x + count] == current):
        positions.append(Position(piece.x + count, piece.y + count))
        count += 1

    if(piece.x == 0 or piece.y == 0 or board[piece.y - 1][piece.x - 1] != ''):
        sides_blocked += 1
    if(piece.x + count >= SIZE - 1 or piece.y + count >= SIZE - 1 or board[piece.y + count + 1][piece.x + count + 1] != ''):
        sides_blocked += 1

    return Line(len(positions), sides_blocked, positions)

def getLineD2(piece: Position, board: List[List[str]]) -> Line:
    # Simon's function
    # Works for diagonal line bottom-left to top-right (↗)
    current = board[piece.y][piece.x]

    # Not bottom-leftmost
    if(piece.x != SIZE - 1 and piece.y != 0 and board[piece.y - 1][piece.x + 1] == current):
        return Line(0, 0, [])
    
    positions = [piece]
    sides_blocked = 0
    count = 1
    while(piece.x - count >= 0 and piece.y + count < SIZE and board[piece.y + count][piece.x - count] == current):
        positions.append(Position(piece.x - count, piece.y + count))
        count += 1

    if(piece.x == SIZE - 1 or piece.y == 0 or board[piece.y - 1][piece.x + 1] != ''):
        sides_blocked += 1
    if(piece.x - count - 1 < 0 or piece.y + count + 1 >= SIZE or board[piece.y + count + 1][piece.x - count - 1] != ''):
        sides_blocked += 1

    return Line(len(positions), sides_blocked, positions)

def get_all_lines(board: List[List[str]], player: str) -> List[Line]:
    # Simon's function
    # Takes the current board, and player's character, and
    # return all lines on the board.

    # First get all pieces of our own's position
    lines: List[Line]
    tempLine: Line
    pieces: List[Position]

    lines = []
    pieces = []

    for i in range(SIZE):
        for j in range(SIZE):
            if board[i][j] == player:
                pieces.append(Position(j,i))

    # Then, for every single pieces on the board, check if it has a line
    for piece in pieces:
        tempLine = getLineH(piece, board)
        if tempLine.num_pieces > 1:
            lines.append(tempLine)
        tempLine = getLineV(piece, board)
        if tempLine.num_pieces > 1:
            lines.append(tempLine)
        tempLine = getLineD1(piece, board)
        if tempLine.num_pieces > 1:
            lines.append(tempLine)
        tempLine = getLineD2(piece, board)
        if tempLine.num_pieces > 1:
            lines.append(tempLine)
    return lines 

# ____________________Simon defined functions for making theall lines____________________


def get_opponent(player: str) -> str:
    return 'O' if player == 'X' else 'X'


def find_extension_spot(line: Line, board: List[List[str]]) -> tuple[int, int] | None:
    # Try to extend the line in either direction if the spot is empty
    start = line.positions[0]
    end = line.positions[-1]
    dx = end.x - start.x
    dy = end.y - start.y

    length = len(line.positions)
    if dx != 0:
        dx //= length - 1
    if dy != 0:
        dy //= length - 1

    # Try before start
    x1 = start.x - dx
    y1 = start.y - dy
    if 0 <= x1 < SIZE and 0 <= y1 < SIZE and board[y1][x1] == '':
        return (y1, x1)

    # Try after end
    x2 = end.x + dx
    y2 = end.y + dy
    if 0 <= x2 < SIZE and 0 <= y2 < SIZE and board[y2][x2] == '':
        return (y2, x2)

    return None  # No extension possible


def choose_move(board, player):
    valid = get_valid_moves(board)
    if not valid:
        raise Exception("No valid moves available")

    player_lines = get_all_lines(board, player)
    enemy_lines = get_all_lines(board, get_opponent(player))

    # 1. Win immediately
    for line in player_lines:
        if line.num_pieces == 4 and line.sides_blocked <= 1:
            move = find_extension_spot(line, board)
            if move:
                return move

    # 2. Block enemy win
    for line in enemy_lines:
        if line.num_pieces == 4 and line.sides_blocked <= 1:
            move = find_extension_spot(line, board)
            if move:
                return move

    # 3. Build own lines: Prefer longer lines first
    for i in range(3, 0, -1):
        for line in player_lines:
            if line.num_pieces == i:
                if line.sides_blocked == 0:
                    move = find_extension_spot(line, board)
                    if move:
                        return move
        # 4. Block enemy lines of size i with no side blocked
        for line in enemy_lines:
            if line.num_pieces == i and line.sides_blocked == 0:
                move = find_extension_spot(line, board)
                if move:
                    return move
        
        # 5. Extend player lines of size i with one side blocked
        for line in player_lines:
            if line.num_pieces == i:
                if line.sides_blocked == 1:
                    move = find_extension_spot(line, board)
                    if move:
                        return move

        # 6. Block enemy lines of size i with one side blocked
        for line in enemy_lines:
            if line.num_pieces == i and line.sides_blocked == 1:
                move = find_extension_spot(line, board)
                if move:
                    return move
        

    # 7. Fallback: Prefer move closest to the center
    center = SIZE // 2
    valid.sort(key=lambda move: abs(move[0] - center) + abs(move[1] - center))
    return valid[0]

# ____________________preexisted functions____________________
# def choose_move(board, player):
#     """
#     TODO: Implement your move selection logic.
#     Should return a tuple (row, col) from get_valid_moves(board).
#     """
#     valid = get_valid_moves(board)
#     if not valid:
#         raise Exception("No valid moves available")
#
#     player_lines = get_all_lines(board, player)
#     if player == 'X':
#         enemy_lines = get_all_lines(board, 'O')
#     else:
#         enemy_lines = get_all_lines(board, 'X')
#
#     # add more stuffs
#
#
#     # Example stub: always pick the first one
#     return valid[0]

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