from botPlayer import BotPlayer


class AlphaBetaPlayer(BotPlayer):
    def __init__(self, depth_limit=5, player=2):
        self.depth_limit = depth_limit
        self.player = player

    def algorithm_name(self):
        return "AlphaBeta"

    def choose_move(self, game):
        alpha = float('-inf')
        beta = float('inf')
        best_move = None
        total_calls = 0

        for move in game.get_available_moves():
            game.make_move(move)
            score, n_calls = self.alphabeta(game, 0, False, alpha, beta)
            # print(f'Move:{move}-> score:{score}')
            total_calls += n_calls
            game.undo_move()
            if score > alpha:
                alpha = score
                best_move = move

        return best_move, total_calls

    def alphabeta(self, game, depth, is_maximizing_player, alpha, beta):
        n_calls = 1
        if depth == self.depth_limit or game.is_game_over():
            return game.evaluate_game_state(self.player), n_calls

        if is_maximizing_player:
            max_eval = float('-inf')
            for move in game.get_available_moves():
                game.make_move(move)
                eval_score, n = self.alphabeta(game, depth + 1, False, alpha, beta)
                n_calls += n
                game.undo_move()
                max_eval = max(max_eval, eval_score)
                alpha = max(alpha, eval_score)
                if beta <= alpha:
                    break
            return max_eval, n_calls
        else:
            min_eval = float('inf')
            for move in game.get_available_moves():
                game.make_move(move)
                eval_score, n = self.alphabeta(game, depth + 1, True, alpha, beta)
                n_calls += n
                game.undo_move()
                min_eval = min(min_eval, eval_score)
                beta = min(beta, eval_score)
                if beta <= alpha:
                    break
            return min_eval, n_calls

    def update(self, _move):
        return

