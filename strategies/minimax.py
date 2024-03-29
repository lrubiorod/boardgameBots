from botPlayer import BotPlayer


class MinimaxPlayer(BotPlayer):
    def __init__(self, depth_limit=5, player=2):
        self.depth_limit = depth_limit
        self.player = player

    def algorithm_name(self):
        return "Minimax"

    def choose_move(self, game):
        best_score = float('-inf')
        best_acc_score = float('-inf')
        min_moves = float('inf')
        best_move = None
        total_calls = 0

        for move in game.get_available_moves():
            game.make_move(move)
            score, acc_score, n_moves, n = self.minimax(game, 0, False)
            total_calls += n
            # print(f'Move:{move}-> score:{score}, n_moves:{n_moves}, acc_score:{acc_score}')
            game.undo_move()
            if ((score > best_score) or
                    (score == best_score and score >= 0 and n_moves < min_moves) or
                    (score == best_score and score < 0 and n_moves > min_moves) or
                    (score == best_score and n_moves == min_moves and acc_score > best_acc_score)):
                best_score = score
                best_acc_score = acc_score
                min_moves = n_moves
                best_move = move

        return best_move, total_calls

    def minimax(self, game, depth, is_maximizing_player):
        acc_score = 0
        n_calls = 1
        if depth == self.depth_limit or game.is_game_over():
            score = game.evaluate_game_state(self.player)
            return score, score, depth + 1, n_calls

        if is_maximizing_player:
            best_score = float('-inf')
            min_moves = float('inf')
            for move in game.get_available_moves():
                game.make_move(move)
                score, acc, n_moves, n = self.minimax(game, depth + 1, False)
                n_calls += n
                acc_score += acc
                game.undo_move()
                if score > best_score or (score == best_score and n_moves < min_moves):
                    best_score = score
                    min_moves = n_moves
            return best_score, acc_score, min_moves, n_calls
        else:
            best_score = float('inf')
            min_moves = float('inf')
            for move in game.get_available_moves():
                game.make_move(move)
                score, acc, n_moves, n = self.minimax(game, depth + 1, True)
                n_calls += n
                acc_score += acc
                game.undo_move()
                if score < best_score or (score == best_score and n_moves < min_moves):
                    best_score = score
                    min_moves = n_moves
            return best_score, acc_score, min_moves, n_calls

    def update(self, _move):
        return
