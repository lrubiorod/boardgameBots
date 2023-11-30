from games.tictactoe import TicTacToe
from strategies.minimax import MinimaxPlayer


def main():
    game = TicTacToe()

    player1 = 'human'
    player2 = MinimaxPlayer(depth_limit=9, player=2)

    turn = 1

    while not game.is_game_over():
        game.print_board()

        current_player = player1 if turn == 1 else player2

        if current_player == 'human':
            move = get_player_move(game, turn)
            game.make_move(move, turn)
        else:
            print(f'Move Player {turn} ({current_player.algorithm_name()}): ')
            move, n = current_player.choose_move(game)
            print(f'{current_player.algorithm_name()} strategy used {n} iterations')
            game.make_move(move, turn)

        if game.is_game_over():
            game.print_board()
            if game.current_winner:
                print(f'Player {game.current_winner} won!')
            else:
                print("Its a tie!")
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


if __name__ == "__main__":
    main()
