import pygame
import random
from collections import namedtuple

pygame.init()

Point = namedtuple('Point', 'x, y')
Scores = namedtuple('Scores', 'ai_score, enemy_score')

#rgb colors
WHITE = (255, 255, 255)
RED = (255, 0, 0)
BLACK = (0, 0, 0)

BLOCK_SIZE = 20


class Game:

    def __init__(self, w=640, h=480):
        self.w = w
        self.h = h

        self.display = pygame.display.set_mode((w,h))
        pygame.display.set_caption('Snake')
        self.clock = pygame.time.Clock()
        self.reset()

    def reset(self):
        #initialize game state
        self.score = Scores(0, 0)
        self.food = None
        self.place_food()

    def update_ui(self):
        self.display.fill(BLACK)

        #update snake position

        #update apple position

        #update score

        pygame.display.update()

    def place_food(self):
        x = random.randint(0, (self.w - BLOCK_SIZE) // BLOCK_SIZE) * BLOCK_SIZE
        y = random.randint(0, (self.h - BLOCK_SIZE) // BLOCK_SIZE) * BLOCK_SIZE
        self.food = Point(x, y)

        #check for snakes


    def play_step(self):
        #update snake position


        #check if game over


        #check if apple eaten


        #return game over, score

        pass

    def is_colliding(self, ai, player):
        #check if snake is colliding into other snake

        #check if snake is colliding with self

        #check if snake is colliding with border

        pass



