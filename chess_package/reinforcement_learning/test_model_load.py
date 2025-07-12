from sb3_contrib.ppo_mask import MaskablePPO
from stable_baselines3 import PPO
from env import CustomChessEnv, Piece
from typing import Optional, List

# 1. Load model
time_steps = 100000
# model = PPO.load(f"chess_model_{time_steps}")
model = MaskablePPO.load(f"chess_model_{time_steps}")

# 2. Create environment
env = CustomChessEnv()
custom_board: List[List[Optional[Piece]]] = [[None for _ in range(5)] for _ in range(5)]

# 3. Example manual placement
custom_board[4][0] = Piece("K", "white")
custom_board[4][1] = Piece("P", "white")

custom_board[0][0] = Piece("K", "black")
custom_board[0][1] = Piece("P", "black")

obs = env.set_board(custom_board, turn="white", is_first_turn=True)
print(obs)

# 4. Get observation from env
# obs = env._get_obs()

# 5. Predict move
mask = env.get_action_mask()
action, _ = model.predict(obs, action_masks=mask, deterministic=True)

# 6. Decode and print move
decoded = env.mapper.decode(int(action))
print(
    f"Model move: from {decoded.from_pos} to {decoded.to_pos} with ability {decoded.ability}"
)
