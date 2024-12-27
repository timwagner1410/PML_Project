from collections import deque

class Snake:

    def __init__(
            self,
            init_x: int,
            init_y: int,
            init_length: int,
            init_direction: tuple[int, int] = (1, 0)
    ):
        self.body = deque([(init_x - i, init_y) for i in range(init_length)])
        self.direction = init_direction # (x, y) direction, if e.g. x = 1, y = 0, then moving right

    def move(self, direction: tuple[int, int]) -> None:
        """
        Move the snake in the given direction, update body and direction
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

        """ TO DO: Detect Apples, then do not pop tail """

        # Remove the tail
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
        return new_head in self.body


if __name__ == '__main__':
    snake = Snake(5, 5, 6)
    print(snake.body)
    print(snake.direction)
    snake.move((0, 1)) # up
    snake.move((1, 0)) # right
    print(snake.is_self_colliding((0, -1)))
    snake.move((0, -1)) # down
    print(snake.body)
    print(snake.direction)