from abc import ABC, abstractmethod


class Game(ABC):
    @abstractmethod
    def make_move(self, move, player):
        pass

    @abstractmethod
    def undo_move(self, move):
        pass

    @abstractmethod
    def get_available_moves(self):
        pass

    @abstractmethod
    def is_game_over(self):
        pass

    @abstractmethod
    def evaluate_game_state(self, player):
        pass

    @abstractmethod
    def print_board(self):
        pass

    @abstractmethod
    def copy(self):
        pass

    @abstractmethod
    def next_player(self, player):
        pass
