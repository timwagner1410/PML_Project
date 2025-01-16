import time
import gymnasium as gym
from gymnasium import spaces
import numpy as np
from game import Game

class SnakeEnv(gym.Env):
    metadata = {'render.modes': ['human']}

    def __init__(self, show: bool = True, grid_size=5):
        super(SnakeEnv, self).__init__()
        self.game = Game()
        self.action_space = spaces.Discrete(3)  # 1 = same dir; 2 = left; 3 = right
        self.show_ui = show
        self.ai_score = 0
        self.bot_score = 0
        self.grid_size = grid_size

        # Define the observation space
        num_cells = grid_size * grid_size
        self.observation_space = spaces.Box(low=-1, high=3, shape=(num_cells + 3,), dtype=np.float32)

    def reset(self, seed=None):
        self.game = Game()
        return (self._get_observation(), {})

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
            2: -5,
            1: 10,
            0: 0.02,
            -1: -10,
            -2: 8
        }

        reward = rewards[self.game.game_state]

        # Update scores based on game state
        if self.game.game_state == 1:
            self.ai_score += 1
        elif self.game.game_state == -1:
            self.bot_score += 1

        terminated = done
        truncated = False  # Set this to True if you have a time limit or other truncation condition

        return obs, reward, terminated, truncated, {}

    def render(self, mode='human'):
        self.game.update_ui()
        time.sleep(0.05)  # Add a delay

    def _get_observation(self):
        if self.show_ui:
            self.render()
        head_x, head_y = self.game.snake_1.body[0]
        half_size = self.grid_size // 2
        surrounding = [
            (head_x + dx, head_y + dy)
            for dx in range(-half_size, half_size + 1)
            for dy in range(-half_size, half_size + 1)
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

        # Calculate distance and direction to the apple
        apple_x, apple_y = self.game.apple.x // self.game.block_size, self.game.apple.y // self.game.block_size
        distance_to_apple = np.sqrt((apple_x - head_x) ** 2 + (apple_y - head_y) ** 2)
        direction_to_apple = (apple_x - head_x, apple_y - head_y)

        # Append distance and direction to the observation
        observation.append(distance_to_apple)
        observation.extend(direction_to_apple)

        return np.array(observation)

if __name__ == '__main__':
    env = SnakeEnv()
    env.reset()

    for _ in range(1000):
        env.render()
        obs, reward, done, _, info = env.step(env.action_space.sample())
        if done:
            env.render()
            if np.any(obs == 1):
                print("Game Over! Player 1 wins!")
            elif np.any(obs == -1):
                print("Game Over! Player 2 wins!")
            break
