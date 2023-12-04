import time

from games.tictactoe import TicTacToe
from games.connect4 import ConnectFour
from strategies.minimax import MinimaxPlayer
from strategies.alphabeta import AlphaBetaPlayer


def main():
    game = choose_game()
    player1, player2 = setup_players()
    duration_player_1 = 0
    duration_player_2 = 0

    turn = 1

    while not game.is_game_over():
        game.print_board()

        current_player = player1 if turn == 1 else player2

        if current_player == 'human':
            start_time = time.time()
            move = get_player_move(game, turn)
            end_time = time.time()
            duration = end_time - start_time

            game.make_move(move, turn)
        else:
            print(f'Move Player {turn} ({current_player.algorithm_name()}): ')
            start_time = time.time()
            move, n = current_player.choose_move(game)
            end_time = time.time()
            duration = end_time - start_time

            print(f'{current_player.algorithm_name()} strategy used {n} iterations and took {duration:.6f} seconds')
            game.make_move(move, turn)

        if turn == 1:
            duration_player_1 += duration
        else:
            duration_player_2 += duration

        if game.is_game_over():
            game.print_board()
            if game.current_winner:
                print(f'Player {game.current_winner} won!')
            else:
                print("Its a tie!")

            print(f'Player 1 time: {duration_player_1:.6f}')
            print(f'Player 2 time: {duration_player_2:.6f}')
            break

        turn = 2 if turn == 1 else 1


def get_player_move(game, turn):
    while True:
        try:
            move = int(input(f'Move Player {turn}: ')) - 1
            if move in game.get_available_moves():
                return move
            print("Invalid movement. Try again!")
        except ValueError:
            print("Write a valid number please!")


def choose_game():
    while True:
        try:
            choice = int(input("Which game would you like to play?\n 1: TicTacToe\n 2: Connect4\n"))
            if choice == 1:
                return TicTacToe()
            elif choice == 2:
                return ConnectFour()
            else:
                print("Invalid choice. Please try again.")
        except ValueError:
            print("Write a valid number please!")


def choose_player_type(player_number):
    while True:
        try:
            choice = int(input(f"Choose the type of player {player_number}:\n 1: Human\n 2: Minimax\n 3: AlphaBeta\n"))
            if choice == 1:
                return 'human'
            elif choice == 2:
                return 'minimax'
            elif choice == 3:
                return 'alphabeta'
            else:
                print("Invalid choice. Please try again.")
        except ValueError:
            print("Write a valid number please!")


def choose_depth(player):
    while True:
        try:
            return int(input(f"Choose maximum depth in your algorithm for Player {player}: "))

        except ValueError:
            print("Write a valid number please!")


def setup_players():
    player1 = 'human'
    player2 = 'human'
    player1_type = choose_player_type(1)
    player2_type = choose_player_type(2)

    if player1_type != 'human':
        if player1_type == 'minimax':
            depth_limit = choose_depth(1)
            player1 = MinimaxPlayer(depth_limit, player=1)
        elif player1_type == 'alphabeta':
            depth_limit = choose_depth(1)
            player1 = AlphaBetaPlayer(depth_limit, player=1)

    if player2_type != 'human':
        if player2_type == 'minimax':
            depth_limit = choose_depth(2)
            player2 = MinimaxPlayer(depth_limit, player=2)
        elif player2_type == 'alphabeta':
            depth_limit = choose_depth(2)
            player2 = AlphaBetaPlayer(depth_limit, player=2)

    return player1, player2


if __name__ == "__main__":
    main()
