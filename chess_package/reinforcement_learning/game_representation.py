from typing import List, Tuple, Dict, Optional


class Piece:
    def __init__(self, type: str, color: str, shielded: bool = False):
        self.type = type  # 'K', 'Q', 'R', 'B', 'P'
        self.color = color  # 'white' or 'black'
        self.shielded = shielded
        self.last_shielded_turn: int


class GameState:
    def __init__(self):
        self.board = [[None for _ in range(5)] for _ in range(5)]
        self.turn = "white"
        self.turn_number = 0
        self.abilities_remaining = {"fog": True, "pawnReset": True, "shield": True}
        self.abilities_activated = []  # [{name: ..., turnsLeft: ..., target: ...}]
        self.pawn_initial_positions = {"white": [], "black": []}  # For Pawn Reset
        self.blocked_tiles = []  # For fog simulation
        self.winner = None


class Move:
    def __init__(
        self,
        from_pos: Tuple[int, int],
        to_pos: Tuple[int, int],
        ability: Optional[Dict] = None,
    ):
        self.from_pos = from_pos
        self.to_pos = to_pos
        self.ability = ability  # Example: {"name": "fog", "target": None}


class ActionMapper:
    def __init__(self):
        self.index_to_action: List[
            Tuple[Tuple[int, int], Tuple[int, int], Optional[Dict]]
        ] = []
        self.action_to_index: Dict[str, int] = {}
        self._generate_actions()

    def _generate_actions(self):
        # Move-only actions (from, to)
        for fr in range(5):
            for fc in range(5):
                for tr in range(5):
                    for tc in range(5):
                        move = ((fr, fc), (tr, tc), None)
                        key = self._action_key(move)
                        self.action_to_index[key] = len(self.index_to_action)
                        self.index_to_action.append(move)

        # Abilities
        abilities = ["fog", "pawnReset"]
        for name in abilities:
            key = self._action_key(((-1, -1), (-1, -1), {"name": name, "target": None}))
            self.action_to_index[key] = len(self.index_to_action)
            self.index_to_action.append(
                ((-1, -1), (-1, -1), {"name": name, "target": None})
            )

        # Shield with target
        for r in range(5):
            for c in range(5):
                key = self._action_key(
                    ((-1, -1), (-1, -1), {"name": "shield", "target": (r, c)})
                )
                self.action_to_index[key] = len(self.index_to_action)
                self.index_to_action.append(
                    ((-1, -1), (-1, -1), {"name": "shield", "target": (r, c)})
                )

    # Encoders & decoders for encoding/decoding the moves
    def _action_key(
        self, action: Tuple[Tuple[int, int], Tuple[int, int], Optional[Dict]]
    ) -> str:
        fr, to, ab = action
        return f"{fr}->{to}:{ab}"

    def encode(self, move: Move) -> int:
        key = self._action_key((move.from_pos, move.to_pos, move.ability))
        return self.action_to_index.get(key, -1)

    def decode(self, index: int) -> Move:
        fr, to, ab = self.index_to_action[index]
        return Move(fr, to, ab)
