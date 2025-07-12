import pandas as pd
import matplotlib.pyplot as plt
from stable_baselines3 import PPO
from stable_baselines3.common.evaluation import evaluate_policy
from stable_baselines3.common.monitor import load_results
from stable_baselines3.common.results_plotter import ts2xy
from stable_baselines3.common.monitor import Monitor

from env import CustomChessEnv

import matplotlib.pyplot as plt
import os
import numpy as np


def evaluate(time_steps: int):
    # Reload the saved model
    model = PPO.load(f"chess_model_{time_steps}")
    env = CustomChessEnv()
    env = Monitor(env, filename="./tensorboard_logs/")

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


def plot_advanced_rewards(log_dir, window=50, show_std=True, save_path=None):
    """
    Plot the reward curve from Monitor logs.

    Args:
        log_dir (str): Directory with Monitor logs.
        window (int): Smoothing window size (moving average).
        show_std (bool): Whether to plot std deviation band.
        save_path (str or None): If provided, saves the figure to this path.
    """
    if not os.path.exists(log_dir):
        raise ValueError(f"Log dir {log_dir} does not exist.")

    data = load_results(log_dir)
    x, y = ts2xy(data, "timesteps")

    if len(x) == 0:
        print("No training data found.")
        return

    # Compute moving average
    y_ma = np.convolve(y, np.ones(window) / window, mode="valid")
    x_ma = x[window - 1 :]

    # Optional std band
    std = []
    if show_std:
        for i in range(len(y_ma)):
            start = max(0, i - window + 1)
            std.append(np.std(y[start : i + 1]))
        std = np.array(std)

    # Plot
    plt.figure(figsize=(10, 6))
    plt.plot(x_ma, y_ma, label="Smoothed Reward", color="blue")
    if show_std:
        plt.fill_between(
            x_ma, y_ma - std, y_ma + std, alpha=0.2, color="blue", label="±1 std dev"
        )

    plt.xlabel("Timesteps")
    plt.ylabel("Episode Reward")
    plt.title("Training Reward Progress")
    plt.grid(True)
    plt.legend()

    if save_path:
        plt.savefig(save_path)
        print(f"Plot saved to {save_path}")
    else:
        plt.show()


if __name__ == "__main__":
    # plot_rewards("./tensorboard_logs")
    plot_advanced_rewards("./tensorboard_logs")
    # evaluate(100000)
