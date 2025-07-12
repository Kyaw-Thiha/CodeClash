import stable_baselines3 as sb3
from env import CustomChessEnv

env = CustomChessEnv(sophisticated_rewards=True)

model = sb3.PPO("CnnPolicy", env, verbose=1)
model.learn(total_timesteps=100_000)
