import pandas as pd
import matplotlib.pyplot as plt
from stable_baselines3 import PPO
from stable_baselines3.common.evaluation import evaluate_policy
from stable_baselines3.common.monitor import load_results
from stable_baselines3.common.results_plotter import ts2xy

from env import CustomChessEnv


def evaluate():
    # Reload the saved model
    model = PPO.load("chess_model")
    env = CustomChessEnv()

    # Evaluate with deterministic policy
    mean_reward, std_reward = evaluate_policy(
        model, env, n_eval_episodes=10, render=False
    )
    print(f"Mean Reward: {mean_reward:.2f} ± {std_reward:.2f}")


def plot_rewards(log_dir):
    data = load_results(log_dir)
    x, y = ts2xy(data, "timesteps")
    plt.plot(x, y)
    plt.xlabel("Timesteps")
    plt.ylabel("Rewards")
    plt.title("Training Reward Progress")
    plt.grid(True)
    plt.show()


if __name__ == "__main__":
    plot_rewards("./tensorboard_logs")
    evaluate()
