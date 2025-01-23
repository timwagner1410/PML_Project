import time

import gymnasium as gym
from gymnasium import spaces
import numpy as np
from game import Game

class SnakeEnv(gym.Env):
    metadata = {'render.modes': ['human']}

    def __init__(self, show: bool = True):
        super(SnakeEnv, self).__init__()
        self.game = Game()
        self.action_space = spaces.Discrete(3)  # 1 = same dir; 2 = left; 3 = right
        self.show_ui = show
        self.ai_score = 0
        self.bot_score = 0

        # Define the observation space
        self.observation_space = spaces.Box(low=-1, high=3, shape=(self.game.h // self.game.block_size +2, self.game.w // self.game.block_size +2), dtype=np.int32)

    def reset(self, seed=None):
        self.game = Game()
        return self._get_observation(), {}


    def step(self, action: object) -> object:

        if action == 1:  # maintain current direction
            pass
        elif action == 2:  # turn left
            self.game.snake_1.direction = (-self.game.snake_1.direction[1], self.game.snake_1.direction[0])
        elif action == 0:  # turn right
            self.game.snake_1.direction = (self.game.snake_1.direction[1], -self.game.snake_1.direction[0])

        self.game.play_step()
        obs = self._get_observation()
        done = abs(self.game.game_state) == 1

        # reward function for snake 1
        """
            2: Snake of Player 2 gets Apple
            1: Snake of Player 2 collides
            0: Nothing happens
            -1: Snake of Player 1 collides
            -2: Snake of Player 1 gets Apple
        """
        rewards = {
            2: 0,
            1: 50,
            0: 1,
            -1: -30,
            -2: 8
        }

        reward = rewards[self.game.game_state]

        if self.game.game_state == 1:
            self.ai_score += 1
        elif self.game.game_state == -1:
            self.bot_score += 1

        terminated = done
        truncated = False  # Set this to True if you have a time limit or other truncation condition

        return obs, reward, terminated, truncated, {}

    def render(self, mode='human'):
        self.game.update_ui()
        time.sleep(0.1)  # Add a delay

    def _get_observation(self):
        if self.show_ui:
            self.render()

        observation = np.zeros((self.game.h // self.game.block_size + 2, self.game.w // self.game.block_size + 2),
                               dtype=np.int32)

        for y in range(self.game.h // self.game.block_size + 2):
            for x in range(self.game.w // self.game.block_size + 2):
                if x == 0 or x == (self.game.w // self.game.block_size) + 1 or y == 0 or y == (
                        self.game.h // self.game.block_size) + 1:
                    observation[y, x] = -1  # Wall
                else:
                    cell = (x - 1, y - 1)
                    if cell in self.game.snake_1.body:
                        observation[y, x] = 1  # AI snake body
                    elif cell in self.game.snake_2.body:
                        observation[y, x] = 2  # Player snake body
                    elif cell == (self.game.apple.x // self.game.block_size, self.game.apple.y // self.game.block_size):
                        observation[y, x] = 3  # Apple
                    else:
                        observation[y, x] = 0

        return observation

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
