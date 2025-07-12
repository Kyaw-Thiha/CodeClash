from stable_baselines3.common.torch_layers import BaseFeaturesExtractor

import torch as th
import torch.nn as nn
import gymnasium as gym

from sb3_contrib.common.maskable.policies import MaskableActorCriticPolicy


class CustomCNNFeatureExtractor(BaseFeaturesExtractor):
    def __init__(self, observation_space: gym.spaces.Box, features_dim: int = 256):
        super().__init__(observation_space, features_dim)

        self.cnn = nn.Sequential(
            nn.Conv2d(in_channels=10, out_channels=32, kernel_size=3, padding=1),
            nn.ReLU(),
            nn.Conv2d(32, 64, kernel_size=3, padding=1),
            nn.ReLU(),
            nn.Flatten(),
        )

        # Calculate flattened feature size
        with th.no_grad():
            sample_input = th.as_tensor(observation_space.sample()[None]).float()
            n_flatten = self.cnn(sample_input).shape[1]

        self.linear = nn.Sequential(
            nn.Linear(n_flatten, features_dim),
            nn.ReLU(),
        )

    def forward(self, observations: th.Tensor) -> th.Tensor:
        return self.linear(self.cnn(observations))


from stable_baselines3.common.policies import ActorCriticPolicy


class CustomCNNPolicy(MaskableActorCriticPolicy):
    def __init__(self, *args, **kwargs):
        super().__init__(
            *args,
            **kwargs,
            features_extractor_class=CustomCNNFeatureExtractor,
            features_extractor_kwargs={"features_dim": 256},
        )
