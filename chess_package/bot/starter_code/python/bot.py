#!/usr/bin/env python3
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
    raise NotImplementedError("setup_phase() not implemented yet")


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
    raise NotImplementedError("play_phase() not implemented yet")


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
    except Exception:
        sys.exit(3)


if __name__ == '__main__':
    main()