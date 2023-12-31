import pygame
import random
import numpy as np
from snake.utils import Direction, Point
from snake.colors import WHITE, BLACK, BLUE1, BLUE2, RED

pygame.init()
font = pygame.font.SysFont("arial", 25)

BLOCK_SIZE = 20  # Size of a square on a display
SPEED = 60  # Speed of the snake


class SnakeGameAI:
    def __init__(self, w=640, h=480):
        self.w = w
        self.h = h

        self.display = pygame.display.set_mode((self.w, self.h))
        pygame.display.set_caption("Snake")
        self.clock = pygame.time.Clock()
        self.reset()

    def reset(self):
        self.direction = Direction.RIGHT

        self.head = Point(self.w / 2, self.h / 2)
        self.snake = [
            self.head,
            Point(self.head.x - BLOCK_SIZE, self.head.y),
            Point(self.head.x - 2 * BLOCK_SIZE, self.head.y),
        ]

        self.score = 0
        self.food = None
        self._place_food()
        self.frame_iteration = 0

    def _place_food(self):
        x = random.randint(0, (self.w - BLOCK_SIZE) // BLOCK_SIZE) * BLOCK_SIZE
        y = random.randint(0, (self.h - BLOCK_SIZE) // BLOCK_SIZE) * BLOCK_SIZE
        self.food = Point(x, y)

        if self.food in self.snake:
            self._place_food()

    def _invert_snake(self):
        self.snake.reverse()
        self.head = self.snake[0]

    def is_collision(self, pt=None):
        if self.head in self.snake[1:]:
            return True
        return False

    def _update_ui(self):
        self.display.fill(BLACK)

        for point in self.snake:
            pygame.draw.rect(
                self.display,
                BLUE1,
                pygame.Rect(point.x, point.y, BLOCK_SIZE, BLOCK_SIZE),
            )
            pygame.draw.rect(
                self.display,
                BLUE2,
                pygame.Rect(point.x + 4, point.y + 4, 12, 12),
            )
            pygame.draw.rect(
                self.display,
                RED,
                pygame.Rect(self.food.x, self.food.y, BLOCK_SIZE, BLOCK_SIZE),
            )

            text = font.render("Score " + str(self.score), True, WHITE)
            self.display.blit(text, [0, 0])
            pygame.display.flip()

    def _move(self, action):
        # straight, back, right, left
        clock_wise = [Direction.RIGHT, Direction.DOWN, Direction.LEFT, Direction.UP]
        idx = clock_wise.index(self.direction)

        if np.array_equal(action, [1, 0, 0, 0]):
            new_dir = clock_wise[idx]  # no change
        elif np.array_equal(action, [0, 1, 0, 0]):
            next_idx = (idx + 1) % 4
            new_dir = clock_wise[next_idx]  # right turn: r>d>l>u
        elif np.array_equal(action, [0, 0, 1, 0]):
            next_idx = (idx - 1) % 4  # turn left: r>u>l>d
            new_dir = clock_wise[next_idx]
        else:
            next_idx = (idx + 2) % 4  # invert direction: u>d, d>u, l>r, r>l
            new_dir = clock_wise[next_idx]
            self._invert_snake()

        self.direction = new_dir

        x = self.head.x
        y = self.head.y

        if self.direction == Direction.RIGHT:
            x += BLOCK_SIZE
            if x > self.w - BLOCK_SIZE:
                x = BLOCK_SIZE
        elif self.direction == Direction.LEFT:
            x -= BLOCK_SIZE
            if x < 0:
                x = self.w - BLOCK_SIZE
        elif self.direction == Direction.DOWN:
            y += BLOCK_SIZE
            if y > self.h - BLOCK_SIZE:
                y = BLOCK_SIZE
        elif self.direction == Direction.UP:
            y -= BLOCK_SIZE
            if y < 0:
                y = self.h - BLOCK_SIZE

        self.head = Point(x, y)
        self.snake.insert(0, self.head)

    def play_step(self, action):
        self.frame_iteration += 1
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()

        self._move(action)

        reward = 0
        game_over = False

        # Bit itself
        if self.is_collision():
            game_over = True
            reward = -50
            return reward, game_over, self.score

        # Ate the food
        elif self.head == self.food:
            reward = 100
            self.score += 1
            self._place_food()
            self.frame_iteration = 0

        # Too long
        elif self.frame_iteration > 100 * len(self.snake):
            game_over = True
            reward = -10
            return reward, game_over, self.score
        else:
            self.snake.pop()

        self._update_ui()
        self.clock.tick(SPEED)

        return reward, game_over, self.score
