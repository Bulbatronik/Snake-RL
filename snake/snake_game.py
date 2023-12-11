import pygame
import random
from enum import Enum
from collections import namedtuple

pygame.init()
font = pygame.font.SysFont("arial", 25)


class Direction(Enum):
    RIGHT = 1
    LEFT = 2
    UP = 3
    DOWN = 4


Point = namedtuple("Point", "x, y")
BLOCK_SIZE = 20
SPEED = 10


WHITE = (255, 255, 255)
RED = (200, 0, 0)
BLUE1 = (0, 0, 255)
BLUE2 = (0, 100, 255)
BLACK = (0, 0, 0)


class SnakeGame:
    def __init__(self, w=640, h=480):
        self.w = w
        self.h = h

        self.display = pygame.display.set_mode((self.w, self.h))
        pygame.display.set_caption("Snake")
        self.clock = pygame.time.Clock()

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

    def _place_food(self):
        x = random.randint(0, (self.w - BLOCK_SIZE) // BLOCK_SIZE) * BLOCK_SIZE
        y = random.randint(0, (self.h - BLOCK_SIZE) // BLOCK_SIZE) * BLOCK_SIZE
        self.food = Point(x, y)

        if self.food in self.snake:
            self._place_food()

    def play_step(self):
        for event in pygame.event.get():
            # if event.type == pygame.QUIT:
            #    pygame.quit()
            #   quit()
            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_LEFT:
                    if self.direction == Direction.RIGHT:
                        self._swap_direction()
                    self.direction = Direction.LEFT
                elif event.key == pygame.K_RIGHT:
                    if self.direction == Direction.LEFT:
                        self._swap_direction()
                    self.direction = Direction.RIGHT
                elif event.key == pygame.K_UP:
                    if self.direction == Direction.DOWN:
                        self._swap_direction()
                    self.direction = Direction.UP
                elif event.key == pygame.K_DOWN:
                    if self.direction == Direction.UP:
                        self._swap_direction()
                    self.direction = Direction.DOWN

        self._move(self.direction)

        game_over = False
        if self._is_collision():
            game_over = True
            return game_over, self.score

        if self.head == self.food:
            self.score += 1
            self._place_food()
        else:
            self.snake.pop()

        self._update_ui()
        self.clock.tick(SPEED)

        return game_over, self.score

    def _swap_direction(self):
        self.head, self.snake[-1] = self.snake[-1], self.head
        self.snake[0] = self.head

    def _is_collision(self):
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

    def _move(self, direction):
        x = self.head.x
        y = self.head.y

        if direction == Direction.RIGHT:
            x += BLOCK_SIZE
            if x > self.w - BLOCK_SIZE:
                x = BLOCK_SIZE
        elif direction == Direction.LEFT:
            x -= BLOCK_SIZE
            if x < 0:
                x = self.w - BLOCK_SIZE
        elif direction == Direction.DOWN:
            y += BLOCK_SIZE
            if y > self.h - BLOCK_SIZE:
                y = BLOCK_SIZE
        elif direction == Direction.UP:
            y -= BLOCK_SIZE
            if y < 0:
                y = self.h - BLOCK_SIZE

        self.head = Point(x, y)
        self.snake.insert(0, self.head)
