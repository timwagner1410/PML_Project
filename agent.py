import gymnasium as gym
from gymnasium import spaces
import numpy as np
from game import Game

class SnakeEnv(gym.Env):
    metadata = {'render.modes': ['human']}

    def __init__(self):
        super(SnakeEnv, self).__init__()
        self.game = Game()
        self.action_space = spaces.Discrete(3)  # 3 possible actions: neutral, left, right (based on current direction)
        self.observation_space = spaces.Box(low=0, high=255, shape=(self.game.height, self.game.width, 3), dtype=np.uint8)

    def reset(self):
        self.game.reset()
        return self._get_observation()

    def step(self, action):
        reward, done = self.game.play_step(action)
        obs = self._get_observation()
        return obs, reward, done, {}

    def render(self, mode='human'):
        self.game.render()

    def _get_observation(self):
        return self.game.get_state()