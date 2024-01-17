from abc import ABC, abstractmethod


class Game(ABC):
    @abstractmethod
    def make_move(self, move):
        pass

    @abstractmethod
    def undo_move(self):
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
    def copy(self, track_previous_state):
        pass

    @abstractmethod
    def get_current_player(self):
        pass

    @abstractmethod
    def get_winner(self):
        pass

    @abstractmethod
    def game_name(self):
        pass

    @abstractmethod
    def process_user_input(self, user_input):
        pass
