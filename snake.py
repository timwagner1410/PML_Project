from collections import deque
import random

class Snake:

    def __init__(
            self,
            init_x: int,
            init_y: int,
            init_length: int,
            init_direction: tuple[int, int] = (-1, 0)
    ):
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

        while ((new_direction[0] == -direction[0] and new_direction[1] == -direction[1])
               or (new_direction[0] == 0 and new_direction[1] == 0)
               or (new_direction[0] != 0 and new_direction[1] != 0)
               or self.is_self_colliding(new_direction)
               or not (0 <= self.body[0][0] + new_direction[0] < width // block_size)
               or not (0 <= self.body[0][1] + new_direction[1] < height // block_size)):
            new_direction = (random.randint(-1, 1), random.randint(-1, 1))

        return new_direction


if __name__ == '__main__':
    snake = Snake(5, 5, 5)
    print(snake.body)