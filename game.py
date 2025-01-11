import pygame
import random
from collections import namedtuple
from snake import PlayerSnake, BotSnake, Snake

pygame.init()

Point = namedtuple('Point', 'x, y')
Scores = namedtuple('Scores', 'player_1_score, player_2_score')

#rgb colors
WHITE = (255, 255, 255)
RED = (255, 0, 0)
BLUE = (0, 0, 255)
GREEN = (0, 255, 0)
BLACK = (0, 0, 0)

BLOCK_SIZE = 30
human_player = True


class Game:

    def __init__(self, w=600, h=480):
        self.w = w
        self.h = h

        assert self.w % BLOCK_SIZE == 0, "Width not divisible by block size"
        assert self.h % BLOCK_SIZE == 0, "Height not divisible by block size"

        if not human_player:
            self.snake_1 = BotSnake(10, 10, 5, (0, 1))
        else:
            self.snake_1 = PlayerSnake(15, 10, 5, (0, 1))

        self.snake_2 = BotSnake(12, 12, 5, (1, 0))

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
        if (x, y) in self.snake_1.body or (x, y) in self.snake_2.body:
            self.place_food()
        else:
            self.apple = Point(x, y)

    def handle_events(self, player: Snake) -> None:
        """
        Enables a Player to control the snake using arrow keys
        :param player: PlayerSnake object
        """

        if not isinstance(player, PlayerSnake):
            return

        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                quit()
            elif event.type == pygame.KEYDOWN:
                if event.key == pygame.K_LEFT and not player.direction == (1, 0):
                    player.change_direction((-1, 0))
                elif event.key == pygame.K_RIGHT and not player.direction == (-1, 0):
                    player.change_direction((1, 0))
                elif event.key == pygame.K_UP and not player.direction == (0, 1):
                    player.change_direction((0, -1))
                elif event.key == pygame.K_DOWN and not player.direction == (0, -1):
                    player.change_direction((0, 1))


    def play_step(self):

        # get new direction for snake
        if not human_player and isinstance(self.snake_1, BotSnake):
            snake_1_dir = self.snake_1.get_random_direction((self.w, self.h, BLOCK_SIZE))
        else:
            assert isinstance(self.snake_1, PlayerSnake), "Player 1 is not a PlayerSnake"
            self.handle_events(self.snake_1)
            snake_1_dir = self.snake_1.direction

        snake_2_dir = self.snake_2.get_random_direction((self.w, self.h, BLOCK_SIZE))

        # check if game over
        game_over = self.is_colliding(snake_1_dir, snake_2_dir)

        # check if apple eaten
        if game_over == -2:
            print(f"Snake 1 gets Apple")
            self.score = Scores(self.score.player_1_score + 1, self.score.player_2_score)
            self.place_food()

        elif game_over == 2:
            print(f"Snake 2 gets Apple")
            self.score = Scores(self.score.player_1_score, self.score.player_2_score + 1)
            self.place_food()

        # move snake
        self.snake_1.move(snake_1_dir, game_over == -2)
        self.snake_2.move(snake_2_dir, game_over == 2)

        # return game over, score
        return game_over, self.score

    def is_colliding(self, direction_snake_1: tuple[int, int], direction_snake_2: tuple[int, int]) -> int:
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
            print("Snake 1 collides with itself")
            return -1

        # Check if snake 2 is colliding with itself
        if self.snake_2.is_self_colliding(direction_snake_2):
            print("Snake 2 collides with itself")
            return 1

        # check for collision of snake 1 with the border
        if head_1_x < 0 or head_1_x >= self.w // BLOCK_SIZE or head_1_y < 0 or head_1_y >= self.h // BLOCK_SIZE:
            print("Snake 1 collides with border")
            return -1

        # check for collision of snake 2 with the border
        if head_2_x < 0 or head_2_x >= self.w // BLOCK_SIZE or head_2_y < 0 or head_2_y >= self.h // BLOCK_SIZE:
            print("Snake 2 collides with border")
            return 1

        # Check if snake 1 is colliding with snake 2
        if (head_1_x, head_1_y) in self.snake_2.body:
            print("Snake 1 collides into Snake 2")
            return -1

        # Check if snake 2 is colliding with snake 1
        if (head_2_x, head_2_y) in self.snake_1.body:
            print("Snake 2 collides into Snake 1")
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

        if game_over == 1:
            raise Exception("Game Over: Winner is Player 1 (blue)")
        elif game_over == -1:
            raise Exception("Game Over: Winner is Player 2 (green)")
        else:
            game.clock.tick(5)
            game_over, score = game.play_step()