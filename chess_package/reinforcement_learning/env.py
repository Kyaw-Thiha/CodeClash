from enum import Enum

import numpy as np

import gymnasium as gym
from gymnasium import spaces

from game_representation import Piece, GameState, Move, ActionMapper
from game_mechanics import get_legal_moves

import random
from typing import Any, Optional, List

# def _place_pieces(self):
#     """
#     A function to place the piece at the start of the game
#     """
#     for c, piece in enumerate(["R", "B", "K", "B", "R"]):
#         self.board[0][c] = Piece(piece, "black")
#         self.board[4][c] = Piece(piece, "white")
#
#     for c in [0, 2, 4]:
#         if self.board:
#             self.board[1][c] = Piece("P", "black")
#             self.board[3][c] = Piece("P", "white")


class CustomChessEnv(gym.Env):
    def __init__(self, seed=42, sophisticated_rewards=False):
        super().__init__()
        self.rng = random.Random()
        self.seed = self._seed(seed)
        self.board: List[List[Optional[Piece]]] = [
            [None for _ in range(5)] for _ in range(5)
        ]
        self.turn = "white"
        self.done = False
        self.winner = None
        self.fog_turns = {"white": 0, "black": 0}
        self.turn_counter = 0
        self.abilities_remaining = {
            "white": {"fog": True, "pawnReset": True, "shield": True},
            "black": {"fog": True, "pawnReset": True, "shield": True},
        }
        self.pawn_starts = {"white": [], "black": []}
        self.mapper = ActionMapper()
        self.action_space = spaces.Discrete(len(self.mapper.index_to_action))
        self.observation_space = spaces.Box(
            low=0, high=1, shape=(10, 5, 5), dtype=np.float32
        )
        self.sophisticated_rewards = sophisticated_rewards
        self.reset()

    def _seed(self, seed=None):
        self.rng.seed(seed)

    def reset(self, *, seed: Optional[int] = None, options: Optional[dict] = None):
        super().reset(seed=seed)
        self.board: List[List[Optional[Piece]]] = [
            [None for _ in range(5)] for _ in range(5)
        ]
        self.seed = self._seed(seed)
        self.turn = "white"
        self.done = False
        self.winner = None
        self.turn_counter = 0
        self.fog_turns = {"white": 0, "black": 0}
        self.abilities_remaining = {
            "white": {"fog": True, "pawnReset": True, "shield": True},
            "black": {"fog": True, "pawnReset": True, "shield": True},
        }
        self._place_pieces()
        return self._get_obs(), {}

    def _place_pieces(self):
        piece_order = ["K"] + ["R"] * 2 + ["B"] * 2 + ["P"] * 3

        positions = [(r, c) for r in [4, 3] for c in range(5)]
        self.rng.shuffle(positions)
        for pos, piece in zip(positions, piece_order):
            r, c = pos
            self.board[r][c] = Piece(piece, "white")
            if piece == "P":
                self.pawn_starts["white"].append((r, c))

        positions = [(r, c) for r in [1, 0] for c in range(5)]
        self.rng.shuffle(positions)
        for pos, piece in zip(positions, piece_order):
            r, c = pos
            self.board[r][c] = Piece(piece, "black")
            if piece == "P":
                self.pawn_starts["black"].append((r, c))

    def step(self, action: int):
        if self.done:
            return self._get_obs(), 0.0, True, False, {}

        move = self.mapper.decode(action)
        reward = self._apply_move(move)

        terminated = self._check_win()
        truncated = False

        if terminated:
            self.done = True
            reward = 1.0 if self.winner == self.turn else -1.0
        else:
            self._decrement_effects()
            self.turn = "black" if self.turn == "white" else "white"
            self.turn_counter += 1

        return self._get_obs(), reward, terminated, truncated, {}

    def _apply_move(self, move: Move):
        reward = 0.0
        if move.ability:
            name = move.ability["name"]
            if name == "fog" and self.abilities_remaining[self.turn]["fog"]:
                self.fog_turns[self.turn] = 3
                self.abilities_remaining[self.turn]["fog"] = False
            elif (
                name == "pawnReset" and self.abilities_remaining[self.turn]["pawnReset"]
            ):
                self._reset_pawns()
                self.abilities_remaining[self.turn]["pawnReset"] = False
            elif name == "shield" and self.abilities_remaining[self.turn]["shield"]:
                r, c = move.ability["target"]
                piece = self.board[r][c]
                if piece and piece.color == self.turn:
                    piece.shielded = True
                    piece.last_shielded_turn = self.turn_counter
                    self.abilities_remaining[self.turn]["shield"] = False
            return reward

        fr, to = move.from_pos, move.to_pos
        fr_r, fr_c = fr
        to_r, to_c = to
        piece = self.board[fr_r][fr_c]
        target = self.board[to_r][to_c]

        if piece is None or piece.color != self.turn:
            return 0.0

        legal_moves = get_legal_moves(self.board, fr, piece)
        if to not in legal_moves:
            return 0.0

        if target and target.shielded:
            return 0.0

        if self.sophisticated_rewards and target:
            reward += 0.1  # reward for capturing
            if target.type == "K":
                reward += 0.9  # strong bonus for killing king

        self.board[to_r][to_c] = piece
        self.board[fr_r][fr_c] = None

        if piece.type == "P" and (to_r == 0 if piece.color == "black" else to_r == 4):
            piece.type = "Q"
            if self.sophisticated_rewards:
                reward += 0.2  # reward for promotion

        return reward

    def _decrement_effects(self):
        for color in ["white", "black"]:
            if self.fog_turns[color] > 0:
                self.fog_turns[color] -= 1
        # Clear expired shields
        for r in range(5):
            for c in range(5):
                piece = self.board[r][c]
                if (
                    piece
                    and piece.shielded
                    and piece.last_shielded_turn < self.turn_counter
                ):
                    piece.shielded = False

    def _reset_pawns(self):
        for r in range(5):
            for c in range(5):
                p = self.board[r][c]
                if p and p.color == self.turn and p.type == "P":
                    self.board[r][c] = None
        for r, c in self.pawn_starts[self.turn]:
            if self.board[r][c] is None:
                self.board[r][c] = Piece("P", self.turn)

    def _check_win(self):
        kings = {"white": False, "black": False}
        for row in self.board:
            for p in row:
                if p and p.type == "K":
                    kings[p.color] = True
        if not kings["white"]:
            self.winner = "black"
            return True
        if not kings["black"]:
            self.winner = "white"
            return True
        return False

    def _get_obs(self):
        obs = np.zeros((10, 5, 5), dtype=np.float32)
        type_to_plane = {"K": 0, "Q": 1, "R": 2, "B": 3, "P": 4}
        visible = np.zeros((5, 5), dtype=bool)

        if self.fog_turns["black" if self.turn == "white" else "white"] > 0:
            for r in range(5):
                for c in range(5):
                    p = self.board[r][c]
                    if p and p.color == self.turn:
                        for target in get_legal_moves(self.board, (r, c), p):
                            visible[target[0]][target[1]] = True
                        visible[r][c] = True
        else:
            visible[:, :] = True

        for r in range(5):
            for c in range(5):
                piece = self.board[r][c]
                if piece and (piece.color == self.turn or visible[r][c]):
                    plane = type_to_plane[piece.type] + (
                        5 if piece.color != self.turn else 0
                    )
                    obs[plane][r][c] = 1

        return obs
