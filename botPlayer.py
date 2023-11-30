from abc import ABC, abstractmethod


class BotPlayer(ABC):
    @abstractmethod
    def choose_move(self, game):
        pass

    @abstractmethod
    def algorithm_name(self):
        pass
