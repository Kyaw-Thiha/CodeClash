from stable_baselines3 import PPO
from stable_baselines3.common.env_checker import check_env
from stable_baselines3.common.monitor import Monitor
from env import CustomChessEnv
from sb3_contrib.ppo_mask import MaskablePPO
from sb3_contrib.common.wrappers import ActionMasker


def train(time_steps: int):
    print("Loading the environment")

    def mask_fn(env):
        return env.unwrapped.get_action_mask()

    env = CustomChessEnv(sophisticated_rewards=True)
    check_env(env, warn=True)
    env = Monitor(env, filename="./tensorboard_logs/")

    env = ActionMasker(env, mask_fn)

    print("Finished loading the environment")

    print("Training the model")

    model = MaskablePPO(
        "MlpPolicy", env, verbose=1, tensorboard_log="./tensorboard_logs"
    )
    # model.learn(total_timesteps=100_000)
    model.learn(total_timesteps=time_steps)
    print("Finished training the model")

    print("Saving the model")
    model.save(f"chess_model_{time_steps}")
    env.close()
    print("Finished saving the model")


if __name__ == "__main__":
    train(100_000)
