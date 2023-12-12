from trainer.agent import Agent, MAX_MEMORY
from snake.snake_game import SnakeGameAI
from utils import plot
import os

os.environ["KMP_DUPLICATE_LIB_OK"] = "TRUE"


if __name__ == "__main__":
    plot_scores = []
    plot_mean_scores = []
    total_score = 0
    record = 0
    agent = Agent()
    game = SnakeGameAI()

    while True:
        state_old = agent.get_state(game)
        final_move = agent.get_action(state_old)
        reward, done, score = game.play_step(final_move)
        state_new = agent.get_state(game)
        agent.train_short_memory(state_old, final_move, reward, state_new, done)
        agent.remember(state_old, final_move, reward, state_new, done)

        if done:
            game.reset()
            agent.n_games += 1
            agent.train_long_memory()
            agent.epsilon -= 0.5 / MAX_MEMORY * agent.n_games
            print("self.epsilon", agent.epsilon)
            if score > record:
                record = score
                agent.model.save()

            print("Game {} | Score {} | Record {}".format(agent.n_games, score, record))

            plot_scores.append(score)
            total_score += score
            mean_score = total_score / agent.n_games
            plot_mean_scores.append(mean_score)
            plot(plot_scores, plot_mean_scores)
