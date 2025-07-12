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

import random
import gymnasium as gym
from sb3_contrib.ppo_mask import MaskablePPO
from stable_baselines3 import PPO
from env import CustomChessEnv, Piece, Move
from typing import Any, Optional, List, Tuple, Dict
from sb3_contrib.common.wrappers import ActionMasker

BOARD_SIZE = 5


# Functions for get the AI model
def get_raw_env(env: gym.Env) -> CustomChessEnv:
    from typing import cast

    return cast(CustomChessEnv, env.unwrapped)


def load_model(
    board: List[List[Optional[Piece]]],
    turn: str = "white",
    turn_counter: int = 0,
    fog_turns: Optional[Dict[str, int]] = None,
    abilities_remaining: Optional[Dict[str, Dict[str, bool]]] = None,
    pawn_starts: Optional[Dict[str, List[Tuple[int, int]]]] = None,
    done: bool = False,
    winner: Optional[str] = None,
):
    time_steps = 100000
    model = MaskablePPO.load(f"chess_model_{time_steps}")

    env = CustomChessEnv()

    def mask_fn(env):
        return env.unwrapped.get_action_mask()

    env = ActionMasker(env, mask_fn)

    raw_env = get_raw_env(env)
    obs = raw_env.set_board(
        board=board,
        turn=turn,
        turn_counter=turn_counter,
        fog_turns=fog_turns,
        abilities_remaining=abilities_remaining,
        pawn_starts=pawn_starts,
        done=done,
        winner=winner,
    )

    mask = raw_env.get_action_mask()
    action, _ = model.predict(obs, action_masks=mask, deterministic=True)
    move = raw_env.mapper.decode(int(action))

    prev_move = None
    while is_ability_action(move):
        # If it is ability action, we need to keep running the model to get movement
        prev_move = move

        env.step(int(action))
        obs = raw_env.change_turn(turn=turn, turn_counter=turn_counter)

        action, _ = model.predict(obs, action_masks=mask, deterministic=True)
        move = raw_env.mapper.decode(int(action))

    return combine_move_and_ability(move, prev_move)


def is_ability_action(decoded_action):
    (from_pos, to_pos, ability) = decoded_action
    return from_pos == (-1, -1) and to_pos == (-1, -1) and ability is not None


def combine_move_and_ability(move_action, ability_action):
    if ability_action is None:
        return move_action

    (from_pos, to_pos, _) = move_action
    (_, _, ability_dict) = ability_action
    return Move(from_pos=from_pos, to_pos=to_pos, ability=ability_dict)


def json_to_set_board_params(data):
    board_data = data["board"]
    turn = data["playerColor"]
    turn_counter = data["turnNumber"]
    abilities_remain = data["abilitiesRemaining"]

    # Convert board: JSON -> List[List[Piece or None]]
    board = []
    pawn_starts = {"white": [], "black": []}

    for r, row in enumerate(board_data):
        board_row = []
        for c, cell in enumerate(row):
            if cell is None:
                board_row.append(None)
            else:
                piece = Piece(type=cell["type"], color=cell["color"])
                board_row.append(piece)
                if piece.type == "P":
                    pawn_starts[piece.color].append((r, c))
        board.append(board_row)

    # Calculate fog turns from abilitiesActivated
    fog_turns = {"white": 0, "black": 0}
    for a in data.get("abilitiesActivated", []):
        if a["name"] == "fog" and a["turnsLeft"] > fog_turns[turn]:
            fog_turns[turn] = a["turnsLeft"]  # you may need to check who used it

    # Determine if the game is done
    done = False
    winner = None
    kings = {"white": False, "black": False}
    for row in board:
        for cell in row:
            if cell and cell.type == "K":
                kings[cell.color] = True
    if not kings["white"]:
        done = True
        winner = "black"
    elif not kings["black"]:
        done = True
        winner = "white"

    return {
        "board": board,
        "turn": turn,
        "turn_counter": turn_counter,
        "fog_turns": fog_turns,
        "abilities_remaining": {
            "white": dict(abilities_remain),
            "black": dict(abilities_remain),
        },
        "pawn_starts": pawn_starts,
        "done": done,
        "winner": winner,
    }


def move_to_json(move: Move) -> Dict:
    return {
        "move": {"from": list(move.from_pos), "to": list(move.to_pos)},
        "ability": {
            "name": move.ability["name"] if move.ability else None,
            "target": list(move.ability["target"])
            if move.ability and move.ability["target"]
            else None,
        },
    }


def on_board(pos) -> bool:
    """Check if a position is within the board boundaries."""
    r, c = pos
    return 0 <= r < BOARD_SIZE and 0 <= c < BOARD_SIZE


def load_state(path: str) -> Dict[str, Any]:
    """Load and return the game state from the given JSON file."""
    with open(path, "r", encoding="utf-8") as f:
        return json.load(f)


def write_move(move_data: Dict[str, Any]) -> None:
    """Write the chosen move (and ability) to move.json."""
    with open("move.json", "w", encoding="utf-8") as f:
        json.dump(move_data, f)


def findOtherKingColumn(state) -> int:
    r = 0 if state["playerColor"] == "white" else 4
    r2 = 1 if state["playerColor"] == "white" else 3

    # Find column of opponent king
    for row in [r, r2]:
        for x in range(0, 5):
            if state["board"][4 - row][x] == None:
                continue
            if state["board"][4 - row][x]["type"] == "K":
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

    r = 0 if state["playerColor"] == "white" else 4
    r2 = 1 if state["playerColor"] == "white" else 3

    # Step 1
    if state["setupStep"] == 1:
        return {"move": {"from": [0, 3], "to": [r, 2]}}
    # Step 2
    elif state["setupStep"] == 2:
        kingPos = findOtherKingColumn(state)
        return {"move": {"to": [4 - r2, kingPos]}}
    # Step 3
    elif state["setupStep"] == 3:
        kingPos = findOtherKingColumn(state)
        if (
            state["board"][r2][kingPos] == None
            or not state["board"][r2][kingPos]["type"] == "R"
        ):
            return {"move": {"to": [r2, kingPos]}}
        randX = random.randint(0, 4)
        while randX == kingPos:
            randX = random.randint(0, 4)
        return {"move": {"to": [r2, randX]}}
    # Step 4
    elif state["setupStep"] == 4:
        counts = countBishopPawns(state)
        for row in {r, r2}:
            for col in range(0, 4):
                if state["board"][row][col] == None:
                    if counts[0] < 2:
                        return {"move": {"from": [0, 3], "to": [row, col]}}
                    else:
                        return {"move": {"from": [0, 4], "to": [row, col]}}
    return {}


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
    game_state = json_to_set_board_params(state)

    move = load_model(**game_state)
    # from = list(move.from_pos)

    result_json = move_to_json(move)

    return result_json

    # raise NotImplementedError("play_phase() not implemented yet")


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
        phase = state.get("phase")
        if phase == "setup":
            move_data = setup_phase(state)
        else:
            move_data = play_phase(state)

        write_move(move_data)
        sys.exit(0)
    except Exception:
        sys.exit(3)


if __name__ == "__main__":
    main()
