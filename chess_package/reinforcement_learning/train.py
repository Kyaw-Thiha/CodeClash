from stable_baselines3 import PPO
from stable_baselines3.common.env_checker import check_env
from env import CustomChessEnv


def train(time_steps: int):
    print("Loading the environment")
    env = CustomChessEnv(sophisticated_rewards=True)
    check_env(env, warn=True)
    print("Finished loading the environment")

    print("Training the model")
    model = PPO("CnnPolicy", env, verbose=1, tensorboard_log="./tensorboard_logs")
    # model.learn(total_timesteps=100_000)
    model.learn(total_timesteps=time_steps)
    print("Finished training the model")

    print("Saving the model")
    model.save(f"chess_model_{time_steps}")
    env.close()
    print("Finished saving the model")


if __name__ == "__main__":
    train(3000)
