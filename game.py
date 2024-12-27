import pygame
import random
from collections import namedtuple
from snake import Snake

pygame.init()

Point = namedtuple('Point', 'x, y')
Scores = namedtuple('Scores', 'ai_score, enemy_score')

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

        self.snake_ai = Snake(28, 20, 20, (0, 1))
        self.snake_bot = Snake(12, 12, 5, (1, 0))

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
            (self.snake_ai, BLUE),
            (self.snake_bot, GREEN),
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

        #check for snakes


    def play_step(self):

        #update snake position
        bot_movement = (0, 0)
        direction = self.snake_bot.direction

        # make random, but valid movement
        while ((bot_movement[0] == -direction[0] and bot_movement[1] == -direction[1])
               or (bot_movement[0] == 0 and bot_movement[1] == 0)
               or (bot_movement[0] != 0 and bot_movement[1] != 0)
               or self.snake_bot.is_self_colliding(bot_movement)):
            bot_movement = (random.randint(-1, 1), random.randint(-1, 1))

        #check if game over
        game_over = self.is_colliding(bot_movement, (1, 0))

        #check if apple eaten
        if game_over == 2:
            print(f"Bot Snake gets Apple")
            self.score = Scores(self.score.ai_score + 1, self.score.enemy_score)
            self.place_food()

        # move snake
        self.snake_bot.move(bot_movement, game_over == 2)

        #return game over, score
        return game_over, self.score

    def is_colliding(self, bot_direction: tuple[int, int], ai_direction: tuple[int, int]) -> int:
        """
        Check if the snake is colliding with itself, the border or the other snake
        :return:
            2: Bot Snake gets Apple
            1: Bot Snake collides
            0: Nothing happens
            -1: AI Snake collides
            -2: AI Snake gets Apple
        """

        # Check if AI snake is colliding with itself
        if self.snake_ai.is_self_colliding(ai_direction):
            return -1

        # Check if bot snake is colliding with itself
        if self.snake_bot.is_self_colliding(bot_direction):
            return 1

        # Check if AI snake is colliding with the border
        ai_head_x, ai_head_y = self.snake_ai.body[0]
        ai_head_x += ai_direction[0]
        ai_head_y += ai_direction[1]

        if ai_head_x < 0 or ai_head_x >= self.w // BLOCK_SIZE or ai_head_y < 0 or ai_head_y >= self.h // BLOCK_SIZE:
            return -1

        # Check if bot snake is colliding with the border
        bot_head_x, bot_head_y = self.snake_bot.body[0]
        bot_head_x += bot_direction[0]
        bot_head_y += bot_direction[1]

        if bot_head_x < 0 or bot_head_x >= self.w // BLOCK_SIZE or bot_head_y < 0 or bot_head_y >= self.h // BLOCK_SIZE:
            return 1

        # Check if AI snake is colliding with the bot snake
        if (ai_head_x, ai_head_y) in self.snake_bot.body:
            return -1

        # Check if bot snake is colliding with the AI snake
        if (bot_head_x, bot_head_y) in self.snake_ai.body:
            return 1

        # Check if AI snake gets the apple
        if (ai_head_x, ai_head_y) == (self.apple.x // BLOCK_SIZE, self.apple.y // BLOCK_SIZE):
            return -2

        # Check if bot snake gets the apple
        if (bot_head_x, bot_head_y) == (self.apple.x // BLOCK_SIZE, self.apple.y // BLOCK_SIZE):
            return 2

        return 0

if __name__ == '__main__':
    game = Game()
    game_over = 0

    while True:
        game.update_ui()

        if abs(game_over) == 1:
            raise Exception("Game Over")

        game.clock.tick(30)
        print(len(game.snake_bot.body))
        game_over, score = game.play_step()