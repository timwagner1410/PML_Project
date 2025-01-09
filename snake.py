from collections import deque
import random
import math

class Snake:

    def __init__(
            self,
            init_x: int,
            init_y: int,
            init_length: int,
            init_direction: tuple[int, int] = (-1, 0)
    ):
        self.directions = {(1,0),(0,1),(-1,0),(0,-1)}
        self.direction = init_direction # (x, y) direction ranging from -1 to 1
        self.body = deque([(init_x - self.direction[0] * i, init_y - self.direction[1] * i) for i in range(init_length)])

    def move(self, direction: tuple[int, int], apple_eaten: bool) -> None:
        """
        Move the snake in the given direction, update body and direction
        :param apple_eaten: whether apple is eaten, if True, do not pop tail
        :param direction: a tuple of size 2 from -1 to 1
        :return: None
        """

        # Check some edge cases
        assert not (direction[0] == -self.direction[0] and direction[1] == -self.direction[1]), "Opposite direction"
        assert not (direction[0] == 0 and direction[1] == 0), "No direction"

        # Update direction
        self.direction = direction

        # Calculate new head position
        head_x, head_y = self.body[0]
        new_head = (head_x + self.direction[0], head_y + self.direction[1])

        # Add new head to the body
        self.body.appendleft(new_head)

        # Remove the tail
        if not apple_eaten:
            self.body.pop()

    def is_self_colliding(self, direction: tuple[int, int]) -> bool:
        """
        Check if the snake will collide with itself after moving in the given direction
        :param direction: a tuple of size 2 from -1 to 1
        :return: True if collision, False otherwise
        """

        # Calculate new head position
        head_x, head_y = self.body[0]
        new_head = (head_x + direction[0], head_y + direction[1])

        # Check if new head is in the body
        return new_head in list(self.body)[:-1]


class BotSnake(Snake):

    def __init__(self, init_x: int, init_y: int, init_length: int, init_direction: tuple[int, int] = (-1, 0)):
        super().__init__(init_x, init_y, init_length, init_direction)

    def get_random_direction(self, playground_info: tuple[int, int, int]) -> tuple[int, int]:
        """
        Gets a random, but valid direction for the bot snake
        :param playground_info: (width, height, block_size)
        :return: new direction
        """
        width, height, block_size = playground_info
        new_direction = (0, 0)
        direction = self.direction
        tries = 0
        max_tries = 500

        possible_directions = self.directions - {(-direction[0], -direction[1])}

        while (self.is_self_colliding(new_direction)
               or not (0 <= self.body[0][0] + new_direction[0] < width // block_size)
               or not (0 <= self.body[0][1] + new_direction[1] < height // block_size)
                ) and tries < max_tries:
            new_direction = random.choice(list(possible_directions))
            tries += 1

        return new_direction if tries < max_tries else direction

    def get_random_biased_direction(self, playground_info: tuple[int, int, int], apple_location: tuple[int,int]) -> tuple[int, int]:
        """
        Gets a random, but valid direction for the bot snake with bias towards the apple
        :param playground_info: (width, height, block_size)
        :return: new direction
        """

        width, height, block_size = playground_info
        new_direction = (0, 0)
        direction = self.direction
        tries = 0
        max_tries = 500
        bias = 1
        possible_directions = self.directions - {(-direction[0], -direction[1])}

        while (self.is_self_colliding(new_direction)
               or not (0 <= self.body[0][0] + new_direction[0] < width // block_size)
               or not (0 <= self.body[0][1] + new_direction[1] < height // block_size)
        ) and tries < max_tries:
            distances = [(math.sqrt((self.body[0][0] + direction[0] - apple_location[0]) ** 2 + (self.body[0][1] + direction[1] - apple_location[1]) ** 2), direction) for direction in possible_directions]
            distances.sort(key=lambda x: x[0])
            print(distances)
            if random.random() < bias:
                new_direction = distances[0][1]
            else:
                new_direction = random.choice(distances[1:])[1]
            tries += 1
        return new_direction if tries < max_tries else direction

class PlayerSnake(Snake):

    def __init__(self, init_x: int, init_y: int, init_length: int, init_direction: tuple[int, int] = (-1, 0)):
        super().__init__(init_x, init_y, init_length, init_direction)
        self.changed: bool = False # Whether the direction has been changed, set to False after each move

    def change_direction(self, new_direction: tuple[int, int]) -> None:
        """
        Change the direction of the snake
        :param new_direction: a tuple of size 2 from -1 to 1
        :return: None
        """
        # Check some edge cases
        assert not (new_direction[0] == -self.direction[0] and new_direction[1] == -self.direction[1]), "Opposite direction"
        assert not (new_direction[0] == 0 and new_direction[1] == 0), "No direction"

        # Update direction
        self.direction = new_direction
        self.changed = True

if __name__ == '__main__':
    snake = Snake(5, 5, 5)
    print(snake.body)