import time

import gymnasium as gym
from gymnasium import spaces
import numpy as np
from game import Game

class SnakeEnv(gym.Env):
    metadata = {'render.modes': ['human']}

    def __init__(self):
        super(SnakeEnv, self).__init__()
        self.game = Game()
        self.action_space = spaces.Discrete(3)  # 1 = same dir; 2 = left; 3 = right

    def reset(self):
        self.game = Game()
        return self._get_observation()

    def step(self, action):

        if action == 2: # move direction to left
            self.game.snake_1.direction = (-self.game.snake_1.direction[1], self.game.snake_1.direction[0])
        elif action == 3: # move direction to right
            self.game.snake_1.direction = (self.game.snake_1.direction[1], -self.game.snake_1.direction[0])

        self.game.play_step()
        obs = self._get_observation()
        done = abs(obs) == 1

        # reward function for snake 1
        rewards = {
            2: -0.5,
            1: 10,
            0: 0.1,
            -1: -20,
            -2: 1
        }

        reward = rewards[obs]

        print(f"Game State: {obs}, Reward: {reward}")

        return obs, reward, done, {}

    def render(self, mode='human'):
        self.game.update_ui()
        time.sleep(0.3)  # Add a delay of 0.1 seconds

    def _get_observation(self):
        return self.game.game_state

if __name__ == '__main__':
    env = SnakeEnv()
    env.reset()

    for _ in range(1000):
        env.render()
        obs, reward, done, info = env.step(env.action_space.sample())
        if done:
            env.render()
            if obs == 1:
                print("Game Over! Player 1 wins!")
            elif obs == -1:
                print("Game Over! Player 2 wins!")
            break
