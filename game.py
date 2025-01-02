import pygame
import random
from collections import namedtuple
from snake import Snake

pygame.init()

Point = namedtuple('Point', 'x, y')
Scores = namedtuple('Scores', 'player_1 Score, player_2_score')

#rgb colors
WHITE = (255, 255, 255)
RED = (255, 0, 0)
BLUE = (0, 0, 255)
GREEN = (0, 255, 0)
BLACK = (0, 0, 0)

BLOCK_SIZE = 20


class Game:

    def __init__(self, w=640, h=480):
        self.w = w
        self.h = h

        self.snake_1 = Snake(28, 20, 20, (0, 1))
        self.snake_2 = Snake(12, 12, 5, (1, 0))

        self.display = pygame.display.set_mode((w,h))
        pygame.display.set_caption('Snake')
        self.clock = pygame.time.Clock()
        self.reset()

    def reset(self):
        #initialize game state
        self.score = Scores(0, 0)
        self.apple = None
        self.place_food()

    def update_ui(self):
        self.display.fill(BLACK)

        #update snake position
        self.draw_snakes()

        #update apple position
        self.draw_apple()

        #update score

        pygame.display.update()

    def draw_snakes(self) -> None:
        """
        Draw the snakes on the screen
        :return: None
        """

        # Assign colors to snakes
        snakes = [
            (self.snake_1, BLUE),
            (self.snake_2, GREEN),
        ]

        # iterate over snakes
        for snake, color in snakes:

            # iterate over snake body
            for i, point in enumerate(snake.body):

                # Calculate head color to distinguish head from body
                head_color = (max(color[0] - 150, 0), max(color[1] - 150, 0), max(color[2] - 150, 0))

                # Draw the filled rectangle
                pygame.draw.rect(self.display, head_color if i == 0 else color,
                                 pygame.Rect(point[0] * BLOCK_SIZE, point[1] * BLOCK_SIZE, BLOCK_SIZE, BLOCK_SIZE))

                # Draw the outline
                outline_color = (max(0, color[0] - 100), max(0, color[1] - 100), max(0, color[2] - 100))
                pygame.draw.rect(self.display, outline_color,
                                 pygame.Rect(point[0] * BLOCK_SIZE, point[1] * BLOCK_SIZE, BLOCK_SIZE, BLOCK_SIZE), 3)

    def draw_apple(self):
        """ Draw the food on the screen """
        pygame.draw.rect(self.display, RED, pygame.Rect(self.apple.x, self.apple.y, BLOCK_SIZE, BLOCK_SIZE))

    def place_food(self):
        x = random.randint(0, (self.w - BLOCK_SIZE) // BLOCK_SIZE) * BLOCK_SIZE
        y = random.randint(0, (self.h - BLOCK_SIZE) // BLOCK_SIZE) * BLOCK_SIZE
        self.apple = Point(x, y)


    def play_step(self):

        # update snake position
        bot_movement = (0, 0)
        direction = self.snake_2.direction

        # make random, but valid movement
        while ((bot_movement[0] == -direction[0] and bot_movement[1] == -direction[1])
               or (bot_movement[0] == 0 and bot_movement[1] == 0)
               or (bot_movement[0] != 0 and bot_movement[1] != 0)
               or self.snake_2.is_self_colliding(bot_movement)):
            bot_movement = (random.randint(-1, 1), random.randint(-1, 1))

        #check if game over
        game_over = self.is_colliding(bot_movement, (1, 0))

        # check if apple eaten
        if game_over == 2:
            print(f"Bot Snake gets Apple")
            self.score = Scores(self.score.ai_score + 1, self.score.enemy_score)
            self.place_food()

        # move snake
        self.snake_2.move(bot_movement, game_over == 2)

        # return game over, score
        return game_over, self.score

    def is_colliding(self, direction_snake_2: tuple[int, int], direction_snake_1: tuple[int, int]) -> int:
        """
        Check if the snake is colliding with itself, the border or the other snake
        :return:
            2: Snake of Player 2 gets Apple
            1: Snake of Player 2 collides
            0: Nothing happens
            -1: Snake of Player 1 collides
            -2: Snake of Player 1 gets Apple
        """

        # Get head & new position of snake 1
        head_1_x, head_1_y = self.snake_1.body[0]
        head_1_x += direction_snake_1[0]
        head_1_y += direction_snake_1[1]

        # Get head & new position of snake 2
        head_2_x, head_2_y = self.snake_2.body[0]
        head_2_x += direction_snake_2[0]
        head_2_y += direction_snake_2[1]

        # Check if snake 1 is colliding with itself
        if self.snake_1.is_self_colliding(direction_snake_1):
            return -1

        # Check if snake 2 is colliding with itself
        if self.snake_2.is_self_colliding(direction_snake_2):
            return 1

        # check for collision of snake 1 with the border
        if head_1_x < 0 or head_1_x >= self.w // BLOCK_SIZE or head_1_y < 0 or head_1_y >= self.h // BLOCK_SIZE:
            return -1

        # check for collision of snake 2 with the border
        if head_2_x < 0 or head_2_x >= self.w // BLOCK_SIZE or head_2_y < 0 or head_2_y >= self.h // BLOCK_SIZE:
            return 1

        # Check if snake 1 is colliding with snake 2
        if (head_1_x, head_1_y) in self.snake_2.body:
            return -1

        # Check if snake 2 is colliding with snake 1
        if (head_2_x, head_2_y) in self.snake_1.body:
            return 1

        # Check if snake 1 gets the apple
        if (head_1_x, head_1_y) == (self.apple.x // BLOCK_SIZE, self.apple.y // BLOCK_SIZE):
            return -2

        # Check if snake 2 gets the apple
        if (head_2_x, head_2_y) == (self.apple.x // BLOCK_SIZE, self.apple.y // BLOCK_SIZE):
            return 2

        return 0

if __name__ == '__main__':
    game = Game()
    game_over = 0

    while True:
        game.update_ui()

        if abs(game_over) == 1:
            raise Exception("Game Over")

        game.clock.tick(5)
        print(len(game.snake_2.body))
        game_over, score = game.play_step()