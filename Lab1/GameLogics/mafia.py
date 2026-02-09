from time import sleep

from GameLogics.abs_logic import IGameLogic
from Entities.board_game import MafiaBoard
from Entities.game_components import Card
from Entities.player import MafiaPlayer

class MafiaGameLogic(IGameLogic):
    def __init__(self, board: MafiaBoard) -> None:
        if not isinstance(board, MafiaBoard):
            raise TypeError("board must be an instance of MafiaBoard")
        self.board: MafiaBoard = board
    
    