import gymnasium as gym
from sb3_contrib.ppo_mask import MaskablePPO
from stable_baselines3 import PPO
from env import CustomChessEnv, Piece
from typing import Optional, List
from sb3_contrib.common.wrappers import ActionMasker


def get_raw_env(env: gym.Env) -> CustomChessEnv:
    from typing import cast

    return cast(CustomChessEnv, env.unwrapped)


# 1. Load model
time_steps = 100000
# model = PPO.load(f"chess_model_{time_steps}")
model = MaskablePPO.load(f"chess_model_{time_steps}")

# 2. Create environment
env = CustomChessEnv()


def mask_fn(env):
    return env.unwrapped.get_action_mask()


env = ActionMasker(env, mask_fn)
custom_board: List[List[Optional[Piece]]] = [[None for _ in range(5)] for _ in range(5)]

# White First Row
# custom_board[4][0] = Piece("B", "white")
custom_board[4][1] = Piece("R", "white")
custom_board[4][2] = Piece("K", "white")
custom_board[4][3] = Piece("P", "white")
# custom_board[4][4] = Piece("B", "white")

# White Second Row
custom_board[3][0] = Piece("B", "white")
custom_board[3][1] = Piece("R", "white")
custom_board[3][2] = Piece("P", "white")
custom_board[3][3] = Piece("P", "white")
custom_board[3][4] = Piece("B", "white")

# Black First Row
# custom_board[0][0] = Piece("K", "black")
custom_board[0][1] = Piece("R", "black")
custom_board[0][2] = Piece("K", "black")
custom_board[0][3] = Piece("P", "black")
# custom_board[0][4] = Piece("R", "black")

# Black Second Row
custom_board[1][0] = Piece("B", "black")
custom_board[1][1] = Piece("R", "black")
custom_board[1][2] = Piece("P", "black")
custom_board[1][3] = Piece("P", "black")
custom_board[1][4] = Piece("B", "black")

raw_env = get_raw_env(env)
obs = raw_env.set_board(custom_board, turn="white", is_first_turn=True)
print(obs)

# 4. Get observation from env
# obs = env._get_obs()

# 5. Predict move
# mask = raw_env.get_action_mask()
# action, _ = model.predict(obs, action_masks=mask, deterministic=True)
#
# print(action)
# print(mask[action])
# print(raw_env.mapper.decode(action))
#
# if not mask[int(action)]:
#     print("⚠️  Model predicted an illegal move!")
#
# # 6. Decode and print move
# decoded = raw_env.mapper.decode(int(action))
# print(
#     f"Model move: from {decoded.from_pos} to {decoded.to_pos} with ability {decoded.ability}"
# )


def print_board(board, last_move=None):
    """
    Prints the board with optional last_move highlighted.
    last_move: ((from_r, from_c), (to_r, to_c))
    """
    piece_symbols = {
        ("K", "black"): "♔",
        ("Q", "black"): "♕",
        ("R", "black"): "♖",
        ("B", "black"): "♗",
        ("P", "black"): "♙",
        ("K", "white"): "♚",
        ("Q", "white"): "♛",
        ("R", "white"): "♜",
        ("B", "white"): "♝",
        ("P", "white"): "♟︎",
    }

    for r in range(5):
        row_repr = []
        for c in range(5):
            piece = board[r][c]
            if piece:
                sym = piece_symbols.get((piece.type, piece.color), "?")
            else:
                sym = "."

            # Mark last move
            if last_move:
                if (r, c) == last_move[0]:
                    sym = f"[{sym}]"
                elif (r, c) == last_move[1]:
                    sym = f"({sym})"
                else:
                    sym = f" {sym} "
            else:
                sym = f" {sym} "

            row_repr.append(sym)
        print("".join(row_repr))
    print()


for i in range(30):
    print(f"\n===== TURN {i + 1} ({raw_env.turn}) =====")
    mask = raw_env.get_action_mask()
    action, _ = model.predict(obs, action_masks=mask, deterministic=True)

    if not mask[int(action)]:
        print("⚠️  Model predicted an illegal move!")

    move = raw_env.mapper.decode(int(action))
    print(
        f"Model move: from {move.from_pos} to {move.to_pos} with ability {move.ability}"
    )
    last_move = (move.from_pos, move.to_pos)
    print_board(raw_env.board, last_move)

    obs, reward, terminated, truncated, _ = env.step(int(action))

    if terminated or truncated:
        print(f"Game Over! Winner: {raw_env.winner}")
        break
