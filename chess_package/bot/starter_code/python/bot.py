#!/usr/bin/env python3

import random
import traceback
"""
Code Clash Chess Challenge — Python Starter Bot

Welcome to the Code Clash Chess Challenge! This is the official Python starter bot for the
custom 5×5 chess variant used in the competition.

You're free to change **any** part of this code. It's just here to help you get started.

-------------------------------------------
How to package your bot as a single file:
-------------------------------------------
1. Install PyInstaller (if you don’t already have it):
   pip install pyinstaller

2. Package your bot into a one-file executable:
   pyinstaller --onefile bot.py

3. The resulting executable will be located in the `dist/` folder
   (e.g., `dist/bot.exe` on Windows)

For rules and move formats, see the `design_doc.md` file provided.
"""

import json
import sys
from typing import Any, Dict
from piece import Piece, King, Pawn, Bishop, Rook

BOARD_SIZE = 5


def on_board(pos) -> bool:
    """Check if a position is within the board boundaries."""
    r, c = pos
    return 0 <= r < BOARD_SIZE and 0 <= c < BOARD_SIZE


def load_state(path: str) -> Dict[str, Any]:
    """Load and return the game state from the given JSON file."""
    with open(path, 'r', encoding='utf-8') as f:
        return json.load(f)


def write_move(move_data: Dict[str, Any]) -> None:
    """Write the chosen move (and ability) to move.json."""
    with open('move.json', 'w', encoding='utf-8') as f:
        json.dump(move_data, f)


# vvv Our implementation is below vvv



def findOtherKingColumn(state) -> int:
    r = 0 if state["playerColor"] == "white" else 4
    r2 = 1 if state["playerColor"] == "white" else 3

    # Find column of opponent king
    for row in [r, r2]:
        for x in range(0, 5):
            if state["board"][4 - row][x] == None:
                continue
            if state["board"][4 - row][x]["type"] == 'K':
                return x
    return -1

def countBishopPawns(state):
    count = [0, 0]

    r = 0 if state["playerColor"] == "white" else 4
    r2 = 1 if state["playerColor"] == "white" else 3

    for row in [r, r2]:
        for col in range(0, 5):
            if state["board"][row][col] == None:
                continue
            elif state["board"][row][col]["type"] == "B":
                count[0] += 1
            elif state["board"][row][col]["type"] == "P":
                count[1] += 1
    return count

def setup_phase(state: Dict[str, Any]) -> Dict[str, Any]:
    """
    Implement your setup phase strategy here.

    Step 1: Place King
    Step 2: Block opponent tile
    Step 3: Place 2 Rooks
    Step 4: Place 2 Bishops and 3 Pawns

    Return a dict: {'move': {'from': [...], 'to': [row, col]}}
    """
    # TODO: Implement your setup logic
    r = 0 if state["playerColor"] == "white" else 4
    r2 = 1 if state["playerColor"] == "white" else 3

    # Step 1
    if (state["setupStep"] == 1):
        return {"move": {"from": [0, 3], "to": [r, 2]}}
    # Step 2
    elif (state["setupStep"] == 2):
        kingPos = findOtherKingColumn(state)
        return {"move": {"to": [4 - r2, kingPos]}}
    # Step 3
    elif (state["setupStep"] == 3):
        kingPos = findOtherKingColumn(state)
        if state["board"][r2][kingPos] == None or not state["board"][r2][kingPos]["type"] == 'R':
            return {"move": {"to": [r2, kingPos]}}
        randX = random.randint(0, 4)
        while (randX == kingPos):
            randX = random.randint(0, 4)
        return {"move": {"to": [r2, randX]}}
    # Step 4
    elif (state["setupStep"] == 4):
        counts = countBishopPawns(state)
        for row in {r, r2}:
            for col in range(0, 4):
                if state["board"][row][col] == None:
                    if counts[0] < 2:
                        return {"move": {"from": [0, 3], "to": [row, col]}}
                    else:
                        return {"move": {"from": [0, 4], "to": [row, col]}}
        return {}
                    


def makeTurn(frm, toCrd, ability):
    '''
    Returns a play phase return-object, moving object from frm to toCrd,
    using the ability ability, if any.
    '''
    return {
                "move": {"from": frm, "to": toCrd},
                "ability": {"name": ability[0], "target": ability[1]}
            }

# PRIORITY FUNCTION
def prioritizeAttackMoves(moves):
    '''
    Given list of moves (i.e. list of tuples (moveValue, targetType))
    Sort most important moves to the front.
    '''
    sorted = []

    for i in range(0, len(moves)):
        if moves[i][1] == "K":
            sorted.insert(0, i)
            return
        # Bishop
        # Rook
        # Pawn
        if moves[i][1] != "none":
            sorted.insert(0, i)
        else:
            sorted.append(i)
    return sorted


def play_phase(state: Dict[str, Any]) -> Dict[str, Any]:
    """
    Implement your play phase strategy here.

    Choose a legal move and optionally activate one ability.

    Return a dict like:
    {
        'move': {'from': [row, col], 'to': [row, col]},
        'ability': {'name': 'fog' | 'pawnReset' | 'shield' | None, 'target': [row, col] | None}
    }
    """

    # TODO: Implement your play logic
    for i in range(0, 25):
        tile = state["board"][i//5][i%5]

        if (tile == None):
            continue
        if tile["color"] == state["playerColor"]:
            if tile["type"] == 'K':
                piece = King(i%5, i//5)
            elif tile["type"] == 'P':
                piece = Pawn(i%5, i//5)
            elif tile["type"] == 'B':
                piece = Bishop(i%5, i//5)
            elif tile["type"] == 'R':
                piece = Rook(i%5, i//5)
            else:
                print("No piece type")
                piece = Piece(i%5, i//5)
        else:
            continue
            
        frm = [piece.y, piece.x]
        toCrd = []
        moves = piece.getAvailableMoves(state)
        priMoves = prioritizeAttackMoves(moves)

        if len(moves) == 0:
            continue

        if isinstance(piece, King):
            fMove = moves[priMoves[0]]
            toCrd = [frm[0] + fMove[0]//3 -1, frm[1] - fMove[0]%3 - 1]
            return makeTurn(frm, toCrd, (None, None))
        
        elif isinstance(piece, Pawn):
            inc = -1 if state["playerColor"] == "black" else 1
            crds = [[frm[0] + inc, frm[1]-1], [frm[0] + inc, frm[1]], [frm[0] + inc, frm[1]+1]]
            toCrd = crds[moves[priMoves[0]][0]]
            return makeTurn(frm, toCrd, (None, None))
        
        elif isinstance(piece, Bishop):
            inc = []
            for i in priMoves:
                n = moves[i][0]
                if n == 0:
                    continue

                if i == 0:
                    inc = [-n, -n]
                elif i == 1:
                    inc = [-n, n]
                elif i == 2:
                    inc = [n, n]
                elif i == 3:
                    inc = [n, -n]

                toCrd = [frm[0] + inc[0], frm[1] + inc[1]]
                
                return makeTurn(frm, toCrd, (None, None))
            
        elif isinstance(piece, Rook):
            inc = []
            for i in priMoves:
                n = moves[i][0]
                if n == 0:
                    continue

                if i == 0:
                    inc = [-n, 0]
                elif i == 1:
                    inc = [0, n]
                elif i == 2:
                    inc = [n, 0]
                elif i == 3:
                    inc = [0, -n]
                toCrd = [frm[0] + inc[0], frm[1] + inc[1]]

                return makeTurn(frm, toCrd, (None, None))
        
    return makeTurn(frm, toCrd, (None, None))
    
 

def main():
    """
    Entry point for the bot.

    Reads state from file, calls the appropriate phase function, and writes move.json.
    """
    if len(sys.argv) != 2:
        print("Usage: python bot.py /path/to/state.json")
        print("Usage (compiled): ./bot /path/to/state.json")
        sys.exit(1)

    state_path = sys.argv[1]

    try:
        state = load_state(state_path)
    except Exception:
        sys.exit(1)

    try:
        phase = state.get('phase')
        if phase == 'setup':
            move_data = setup_phase(state)
        else:
            move_data = play_phase(state)

        write_move(move_data)
        sys.exit(0)
    except Exception as e:
        print(e)
        traceback.print_exc()
        sys.exit(3)


if __name__ == '__main__':
    main()