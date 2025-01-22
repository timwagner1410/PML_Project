import gym
from gym import spaces
import numpy as np
import time
import math

from game import Game

class SnakeSafetyEnv(gym.Env):
    metadata = {'render.modes': ['human']}

    def __init__(self, show: bool = True):
        super(SnakeSafetyEnv, self).__init__()
        self.show_ui = show
        self.ai_score = 0
        self.bot_score = 0
        self.safety_cost = 0

        # Initialize your custom game logic here
        self.game = Game()  # Replace with your actual game initialization

        # Action space: [Maintain direction, Turn left, Turn right]
        self.action_space = spaces.Discrete(3)

        # Observation space: Include the game grid with walls, snake bodies, and apple
        self.observation_space = spaces.Box(
            low=-1,
            high=3,
            shape=(self.game.h // self.game.block_size + 2, self.game.w // self.game.block_size + 2),
            dtype=np.int32
        )

    def reset(self, seed=None, options=None):
        self.game = Game()  # Reset the game state
        self.safety_cost = 0  # Reset safety cost
        return self._get_observation(), {}

    def step(self, action):
        # Handle snake movement
        if action == 1:  # Maintain current direction
            pass
        elif action == 2:  # Turn left
            self.game.snake_1.direction = (-self.game.snake_1.direction[1], self.game.snake_1.direction[0])
        elif action == 0:  # Turn right
            self.game.snake_1.direction = (self.game.snake_1.direction[1], -self.game.snake_1.direction[0])

        # Perform a step in the game logic
        self.game.play_step()

        # Get the observation
        obs = self._get_observation()

        # Check if the game is over
        done = abs(self.game.game_state) == 1

        # Reward function
        rewards = {
            2: 0,    # Snake of player 2 gets apple
            1: 70,   # Snake of player 2 collides
            0: 1,    # Nothing happens
            -1: -100, # Snake of player 1 collides
            -2: 10  # Snake of player 1 gets apple
        }

        # Safety cost: Add penalties for unsafe behavior
        self.safety_cost += self._calculate_safety_cost()

        reward = rewards[self.game.game_state]
        reward-= self.safety_cost

        # Increment scores
        if self.game.game_state == 1:
            self.ai_score += 1
        elif self.game.game_state == -1:
            self.bot_score += 1


        terminated = done
        truncated = False  # Truncate only if you have a time limit

        # Return the environment state
        return obs, reward, terminated, truncated, {"safety_cost": self.safety_cost}

    def render(self, mode='human'):
        if self.show_ui:
            self.game.update_ui()  # Render the game UI
            time.sleep(0.05)

    def _get_observation(self):
        # Build a grid representing the environment
        observation = np.zeros(
            (self.game.h // self.game.block_size + 2, self.game.w // self.game.block_size + 2),
            dtype=np.int32
        )

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

    def _calculate_safety_cost(self):
        """
        Calculate safety cost based on game state.
        E.g., penalize for hitting walls, hazards, or unsafe areas.
        """
        cost = 0

        distanceToLeftWall = self.game.snake_1.body[0][0] - 0
        distanceToRightWall = self.game.w // self.game.block_size - self.game.snake_1.body[0][0]
        distanceToTopWall = self.game.snake_1.body[0][1] - 0
        distanceToBottomWall = self.game.h // self.game.block_size - self.game.snake_1.body[0][1]

        # Penalize for getting too close to walls
        if distanceToLeftWall < 2 or distanceToRightWall < 2 or distanceToTopWall < 2 or distanceToBottomWall < 2:
            cost += 1

        # Penalize for getting too close to the bot snake
        for body_part in self.game.snake_2.body:
            distance = math.sqrt((self.game.snake_1.body[0][0] - body_part[0])**2 + (self.game.snake_1.body[0][1] - body_part[1])**2)
            if distance < 2:
                cost += 0.5

        # Penalize for getting crashed into itself
        if self.game.snake_1.direction + self.game.snake_1.body[0] in self.game.snake_1.body:
            cost += 50




        return cost