import time
import random
import math

from botPlayer import BotPlayer


class MCTSNode:
    WIN = 10
    LOSE = -10
    DRAW = 0

    def __init__(self, game_state, parent=None, move=None, is_alpha=True):
        self.game_state = game_state
        self.parent = parent
        self.move = move
        self.children = []
        self.wins = 0
        self.visits = 0
        self.untried_moves = game_state.get_available_moves()
        self.result = None
        self.is_alpha = is_alpha

    def add_child(self, move, game_state, player):
        # Alpha when next movement is mine, beta if not
        is_alpha = game_state.get_current_player() == player

        new_node = MCTSNode(game_state, parent=self, move=move, is_alpha=is_alpha)
        self.untried_moves.remove(move)
        self.children.append(new_node)

        # Update definitive state
        if game_state.is_game_over():
            new_node.result = game_state.evaluate_game_state(player) * 10

        return new_node

    def is_fully_expanded(self):
        return len(self.untried_moves) == 0

    def best_child(self, c_param=1.4):
        if c_param == 0:
            return max(self.children,
                       key=lambda child: child.result if child.result is not None else child.wins / child.visits)
        else:
            unresolved_children = [child for child in self.children if child.result is None]

            if not unresolved_children:
                return max(self.children, key=lambda child: child.result if child.result is not None else -float('inf'))

            choices_weights = [
                (child.wins / child.visits) + c_param * (2 * math.log(self.visits) / child.visits) ** 0.5
                for child in unresolved_children
            ]
            return unresolved_children[choices_weights.index(max(choices_weights))]

    def check_parent_propagation(self):
        if self.parent is not None:
            self.parent.check_children_resolved()

    def check_children_resolved(self):
        best_child_result = -float('inf') if self.is_alpha else float('inf')
        all_children_resolved = True
        none_counter = 0

        for child in self.children:
            if child.result is None:
                none_counter += 1
                all_children_resolved = False
            else:
                if self.is_alpha:
                    best_child_result = max(best_child_result, child.result)
                    if child.result == MCTSNode.WIN:
                        self.result = MCTSNode.WIN
                        return
                else:
                    best_child_result = min(best_child_result, child.result)
                    if child.result == MCTSNode.LOSE:
                        self.result = MCTSNode.LOSE
                        return

        if self.is_fully_expanded():
            if self.parent is None and none_counter == 1:
                self.result = MCTSNode.DRAW
            elif all_children_resolved:
                self.result = best_child_result


class MCTSSolverPlayer(BotPlayer):
    def __init__(self, time_limit=5, player=2):
        self.time_limit = time_limit
        self.player = player

    def algorithm_name(self):
        return "MCTS-Solver"

    def choose_move(self, game):
        root = MCTSNode(game.copy(), parent=None, move=None)

        start_time = time.time()
        while time.time() - start_time < self.time_limit:
            if root.result is not None:
                break

            node = root
            temp_game = game.copy()

            # Selection
            while node.is_fully_expanded() and not temp_game.is_game_over():
                node = node.best_child()
                temp_game.make_move(node.move)

            # Expansion
            if not node.is_fully_expanded():
                move = random.choice(node.untried_moves)
                temp_game.make_move(move)

                node = node.add_child(move, temp_game, self.player)

            # Simulation
            while not temp_game.is_game_over():
                temp_game.make_move(random.choice(temp_game.get_available_moves()))

            # Backpropagation
            game_result = temp_game.evaluate_game_state(self.player)
            while node is not None:
                node.visits += 1
                node.wins += game_result
                if node.result is not None:
                    node.check_parent_propagation()

                node = node.parent

        # print_debug(root)

        best_move = root.best_child(c_param=0).move
        return best_move, root.visits


def print_debug(node):
    for child in node.children:
        if child.result == MCTSNode.WIN:
            ratio = "Result Achieved: WIN"
        elif child.result == MCTSNode.LOSE:
            ratio = "Result Achieved: LOSE"
        else:
            win_visit_ratio = child.wins / child.visits if child.visits > 0 else 0
            ratio = f"Win/Visit Ratio: {win_visit_ratio:0.4f}"

        print(f"Move: {child.move}, {ratio}, Visits: {child.visits}, ")
