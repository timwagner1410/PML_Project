import time
import gymnasium as gym
from gymnasium import spaces
import numpy as np
from game import Game

class SafeSnakeEnv(gym.Env):
    metadata = {'render.modes': ['human']}

    def __init__(self, show: bool = True, grid_size=5):
        super(SafeSnakeEnv, self).__init__()
        self.game = Game()
        self.action_space = spaces.Discrete(3)  # 1 = same dir; 2 = left; 3 = right
        self.show_ui = show
        self.ai_score = 0
        self.bot_score = 0
        self.grid_size = grid_size

        # Define the observation space
        num_cells = grid_size * grid_size
        self.observation_space = spaces.Box(low=-1, high=3, shape=(num_cells + 8,), dtype=np.float32)

    def reset(self, seed=None):
        self.game = Game()
        return (self._get_observation(), {})

    def is_deadly(self):
        directions = [
            self.game.snake_1.direction,  # current direction
            (-self.game.snake_1.direction[1], self.game.snake_1.direction[0]),  # left
            (self.game.snake_1.direction[1], -self.game.snake_1.direction[0])  # right
        ]
        deadly = []

        for direction in directions:
            head_x, head_y = self.game.snake_1.body[0]
            new_head_x = head_x + direction[0]
            new_head_y = head_y + direction[1]

            # Check for collision with walls
            if new_head_x < 0 or new_head_x >= self.game.w // self.game.block_size or new_head_y < 0 or new_head_y >= self.game.h // self.game.block_size:
                deadly.append(1)
                continue

            # Check for collision with itself
            if (new_head_x, new_head_y) in self.game.snake_1.body:
                deadly.append(1)
                continue

            # Check for collision with the other snake
            if (new_head_x, new_head_y) in self.game.snake_2.body:
                deadly.append(1)
                continue

            deadly.append(0)

        return deadly

    def step(self, action):
        if action == 1:  # maintain current direction
            pass
        elif action == 2:  # turn left
            self.game.snake_1.direction = (-self.game.snake_1.direction[1], self.game.snake_1.direction[0])
        elif action == 0:  # turn right
            self.game.snake_1.direction = (self.game.snake_1.direction[1], -self.game.snake_1.direction[0])

        self.game.play_step()
        obs = self._get_observation()
        done = abs(self.game.game_state) == 1

        # Calculate distance to the closest cell of the opponent snake
        head_x, head_y = self.game.snake_1.body[0]
        opponent_cells = self.game.snake_2.body
        distances_to_opponent = [np.sqrt((cell[0] - head_x) ** 2 + (cell[1] - head_y) ** 2) for cell in opponent_cells]
        min_distance_to_opponent = min(distances_to_opponent)

        # Adjust reward values based on the distance to the opponent snake
        if min_distance_to_opponent < 3:  # opponent is close
            reward_for_0 = 0.5
            reward_for_apple = 0.05
        else:  # opponent is far
            reward_for_0 = 0.02
            reward_for_apple = 7

        # Calculate distance to the center of the grid
        center_x, center_y = self.game.w // (2 * self.game.block_size), self.game.h // (2 * self.game.block_size)
        distance_to_center = np.sqrt((center_x - head_x) ** 2 + (center_y - head_y) ** 2)

        # Add a small reward for being close to the center
        center_reward = max(0, 1 - distance_to_center / max(center_x, center_y)) * 0.1

        # reward function for snake 1
        rewards = {
            2: 0,
            1: 50,
            0: reward_for_0 + center_reward,
            -1: -50,
            -2: reward_for_apple
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
            elif 0 <= cell[0] < self.game.w // self.game.block_size and 0 <= cell[
                1] < self.game.h // self.game.block_size:
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

        # Append the direction of the AI snake
        direction_snake_1 = self.game.snake_1.direction
        observation.extend(direction_snake_1)

        # Calculate distances to the closest 3 cells of the opponent snake
        opponent_cells = self.game.snake_2.body
        distances_to_opponent = sorted(
            [np.sqrt((cell[0] - head_x) ** 2 + (cell[1] - head_y) ** 2) for cell in opponent_cells]
        )[:3]
        observation.extend(distances_to_opponent)

        # Ensure all elements in observation are of the same type and shape
        observation = [float(x) for x in observation]

        return np.array(observation, dtype=np.float32)

if __name__ == '__main__':
    env = SafeSnakeEnv()
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
