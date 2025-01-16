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

        # Define the observation space
        self.observation_space = spaces.Box(low=-1, high=3, shape=(9,), dtype=np.int32)

    def reset(self, seed=None):
        self.game = Game()
        return self._get_observation(), {}

    def step(self, action):
        if action == 2:  # move direction to left
            self.game.snake_1.direction = (-self.game.snake_1.direction[1], self.game.snake_1.direction[0])
        elif action == 3:  # move direction to right
            self.game.snake_1.direction = (self.game.snake_1.direction[1], -self.game.snake_1.direction[0])

        self.game.play_step()
        obs = self._get_observation()
        done = abs(self.game.game_state) == 1

        # reward function for snake 1
        rewards = {
            2: -0.5,
            1: 10,
            0: 0.1,
            -1: -20,
            -2: 1
        }

        reward = rewards[self.game.game_state]

        # print(f"Game State: {self.game.game_state}, Reward: {reward}")

        terminated = done
        truncated = False  # Set this to True if you have a time limit or other truncation condition

        return obs, reward, terminated, truncated, {}

    def render(self, mode='human'):
        self.game.update_ui()
        time.sleep(0.05)  # Add a delay of 0.1 seconds

    def _get_observation(self):
        head_x, head_y = self.game.snake_1.body[0]
        surrounding = [
            (head_x - 1, head_y - 1), (head_x, head_y - 1), (head_x + 1, head_y - 1),
            (head_x - 1, head_y), (head_x, head_y), (head_x + 1, head_y),
            (head_x - 1, head_y + 1), (head_x, head_y + 1), (head_x + 1, head_y + 1)
        ]
        observation = []
        for cell in surrounding:
            if cell in self.game.snake_1.body:
                observation.append(1)  # AI snake body
            elif cell in self.game.snake_2.body:
                observation.append(2)  # Player snake body
            elif cell == (self.game.apple.x // self.game.block_size, self.game.apple.y // self.game.block_size):
                observation.append(3)  # Apple
            elif 0 <= cell[0] < self.game.w // self.game.block_size and 0 <= cell[1] < self.game.h // self.game.block_size:
                observation.append(0)  # Empty space
            else:
                observation.append(-1)  # Wall

        return np.array(observation)

if __name__ == '__main__':
    env = SnakeEnv()
    env.reset()

    for _ in range(1000):
        env.render()
        obs, reward, done, _, info = env.step(env.action_space.sample())
        if done:
            env.render()
            if obs == 1:
                print("Game Over! Player 1 wins!")
            elif obs == -1:
                print("Game Over! Player 2 wins!")
            break
