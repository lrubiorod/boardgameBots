import time
import random
import math

from botPlayer import BotPlayer


class MCTSNode:
    def __init__(self, game_state, parent=None, move=None):
        self.game_state = game_state
        self.parent = parent
        self.move = move
        self.children = []
        self.wins = 0
        self.visits = 0
        self.untried_moves = game_state.get_available_moves()

    def add_child(self, move, game_state):
        new_node = MCTSNode(game_state, parent=self, move=move)
        self.untried_moves.remove(move)
        self.children.append(new_node)
        return new_node

    def is_fully_expanded(self):
        return len(self.untried_moves) == 0

    def best_child(self, c_param=1.4):
        choices_weights = [
            (child.wins / child.visits) + c_param * (2 * math.log(self.visits) / child.visits) ** 0.5
            for child in self.children
        ]
        return self.children[choices_weights.index(max(choices_weights))]


class MCTSPlayer(BotPlayer):
    def __init__(self, time_limit=5, player=2):
        self.time_limit = time_limit
        self.player = player

    def algorithm_name(self):
        return "MCTS"

    def choose_move(self, game):
        root = MCTSNode(game.copy(), parent=None, move=None)

        # Handle case only 1 option
        if len(root.untried_moves) == 1:
            return root.untried_moves[0], 1

        start_time = time.time()
        while time.time() - start_time < self.time_limit:
            node = root
            temp_game = game.copy()
            first_expansion = True

            # Selection
            while node.is_fully_expanded() and not node.game_state.is_game_over():
                node = node.best_child()
                first_expansion = False
                temp_game.make_move(node.move, self.player)

            # Expansion
            if not node.is_fully_expanded():
                move = random.choice(node.untried_moves)
                temp_game.make_move(move, self.player)

                # Handle case win with 1 movement
                if first_expansion and (temp_game.evaluate_game_state(self.player) == 1):
                    return move, root.visits

                node = node.add_child(move, temp_game)

            # Simulation
            next_player = game.next_player(self.player)
            while not temp_game.is_game_over():
                random_move = random.choice(temp_game.get_available_moves())
                temp_game.make_move(random_move, next_player)
                next_player = game.next_player(next_player)

            # Backpropagation
            while node is not None:
                node.visits += 1
                node.wins += temp_game.evaluate_game_state(self.player)
                node = node.parent

        for child in root.children:
            win_visit_ratio = child.wins / child.visits if child.visits > 0 else 0
            print(
                f"Move: {child.move}, Win/Visit Ratio: {win_visit_ratio:0.4f}, Visits: {child.visits}, ")

        best_move = root.best_child(c_param=0).move
        return best_move, root.visits
