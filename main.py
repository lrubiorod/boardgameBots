import time

from games.tictactoe import TicTacToe
from games.connect4 import ConnectFour
from games.easy_boop import Boop
from strategies.minimax import MinimaxPlayer
from strategies.alphabeta import AlphaBetaPlayer
from strategies.mcts import MCTSPlayer
from strategies.mcts_solver import MCTSSolverPlayer


def main():
    game = choose_game()
    players = [choose_player_type(1), choose_player_type(2)]
    player_duration = [0] * len(players)

    while not game.is_game_over():
        game.print_board()

        turn = game.get_current_player()
        player = players[turn - 1]

        if player == 'human':
            start_time = time.time()
            move = get_player_move(game)
            end_time = time.time()
            duration = end_time - start_time

            if not game.make_move(move):
                print("Invalid movement. Try again!")
        else:
            start_time = time.time()
            move, n = player.choose_move(game)
            end_time = time.time()
            duration = end_time - start_time

            print(f'Move Player {turn} ({player.algorithm_name()}): {move}')
            print(f'{player.algorithm_name()} strategy used {n} iterations and took {duration:.6f} seconds')
            game.make_move(move)

        player_duration[turn - 1] += duration

        if game.is_game_over():
            game.print_board()
            winner = game.get_winner()
            if winner:
                print(f'Player {winner} won!')
            else:
                print("Its a tie!")

            for i, duration in enumerate(player_duration):
                print(f'Player {i +1} time: {duration:.6f}')

            break


def get_player_move(game):
    while True:
        try:
            user_input = input(f'Move Player {game.get_current_player()}: ')
            move = game.process_user_input(user_input)

            if move in game.get_available_moves():
                return move
            else:
                print("Invalid movement. Try again!")
        except ValueError as e:
            print(e)


def choose_game():
    while True:
        try:
            choice = int(input("Which game would you like to play?\n 1: TicTacToe\n 2: Connect4\n 3: Boop\n"))
            if choice == 1:
                return TicTacToe()
            elif choice == 2:
                return ConnectFour()
            elif choice == 3:
                return Boop()
            else:
                print("Invalid choice. Please try again.")
        except ValueError:
            print("Write a valid number please!")


def choose_player_type(player_number):
    while True:
        try:
            choice = int(input(f"Choose the type of player {player_number}:\n 1: Human\n 2: Minimax\n 3: AlphaBeta\n "
                               f"4: MTCS\n 5: MTCS-Solver\n"))
            if choice == 1:
                # Human Player
                return 'human'
            elif choice == 2:
                # Minimax Player
                depth_limit = choose_depth_or_time(player_number)
                return MinimaxPlayer(depth_limit, player=player_number)
            elif choice == 3:
                # AlphaBeta Player
                depth_limit = choose_depth_or_time(player_number)
                return AlphaBetaPlayer(depth_limit, player=player_number)
            elif choice == 4:
                # MCTS Player
                time_limit = choose_depth_or_time(player_number, 'time')
                return MCTSPlayer(time_limit, player=player_number)
            elif choice == 5:
                # MCTS Player
                time_limit = choose_depth_or_time(player_number, 'time')
                return MCTSSolverPlayer(time_limit, player=player_number)
            else:
                print("Invalid choice. Please try again.")
        except ValueError:
            print("Write a valid number please!")


def choose_depth_or_time(player, n='depth'):
    while True:
        try:
            return int(input(f"Choose maximum {n} in your algorithm for Player {player}: "))

        except ValueError:
            print("Write a valid number please!")


if __name__ == "__main__":
    main()
