from snake import SnakeGame
import pygame


def main():
    game = SnakeGame()

    while True:
        game_over, score = game.play_step()

        if game_over:
            break
    print(f"Final Score: {score}")
    pygame.quit()


if __name__ == "__main__":
    main()
