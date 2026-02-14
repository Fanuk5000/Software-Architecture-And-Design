from random import choice
from time import sleep
from typing import Callable

from GameLogics.logic import GameLogic
from Entities.alias_board import AliasBoard
from Entities.player import MonopolyPlayer


class AliasLogic(GameLogic):
    def __init__(self, board: AliasBoard, ui_callback: Callable[[str], None]) -> None:
        if not isinstance(board, AliasBoard):
            raise TypeError("board must be an instance of AliasBoard")
        self._board: AliasBoard = board
        self._ui_callback: Callable[[str], None] = ui_callback

    def is_game_over(self) -> bool:
        for team in self._board.teams:
            if team.chip.chip_position >= 100:
                return True
        return False

    def make_moves(self) -> None:
        pass
