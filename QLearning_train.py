from Ntxuva import Ntxuva
from game import Game
from players import QPlayer, RandomPlayer, MoveConverter

# parameters for game
ALPHA = 0.01
GAMMA = 0.99
EPSILON = 1
ROWS = 4
COLUMNS = 8
SEEDS = 2
EPISODES = 1000

board = Ntxuva(rows=ROWS, columns=COLUMNS, seeds=SEEDS)
ACTION_SPACE = (board.rows // 2) * board.columns

q_player = QPlayer(alpha=ALPHA, gamma=GAMMA, epsilon=EPSILON, Q={}, action_space=ACTION_SPACE)

random_player = RandomPlayer(row1=2, row2=3)

# Initializing the game
game = Game(q_player, random_player, board)

# initializing the move converter ...
move_converter = MoveConverter()


# LETS ASSUME THE PLAYER 1 IS THE Q PLAYER AND THE PLAYER 2 ARE THE RANDOMMN PLAYER
# The player 1 turn is represented by x and the other player by o
# The players 1 row is zero and one and the following 2 and 3 is for player 2
def play_game(player1, player2, env, move_converter, episodes=1000):
    counter = 0

    for episode in range(episodes):
        done = False
        old_state = env.make_key()
        env.reset()
        counter = 0
        while not done:
            # Saving the old state into old_state variable
            counter += 1
            if env.turn == 'x':
                q_player_actions = player1.act(old_state)
                # print(f"ACT ---- {env.turn} -- {counter}")
                action_num = q_player_actions
                action = move_converter.player1_actions.get(q_player_actions)
                # print(f"MOVE --- CONVERTER {env.turn} -- {counter}")

            else:
                action = player2.get_move(env)
            old = env.board

            new_state, reward, done = env.step(action)

            new_state = env.make_key()

            if env.turn == 'x':
                new_state = env.make_key()
                player1.update_policy(old_state, new_state, action_num, reward)

            old_state = new_state

            # convert new state

        #print(f"counter -- {counter} | the winner is {env.declare_winner()}")


play_game(q_player, random_player, board, move_converter=move_converter)
