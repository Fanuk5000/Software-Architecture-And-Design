import textwrap
from typing import (
    Any,
    Callable,
)
from abc import ABC, abstractmethod

from Entities.boards.board import BoardGame


class GameLogic(ABC):
    _board: BoardGame | Any
    _ui_callback: Callable[[str, str], None]

    def _send_to_ui(self, message: str, end: str = "\n") -> None:
        if not isinstance(message, str):
            raise TypeError("message must be a string")
        self._ui_callback(message, end)

    def can_start_game(self) -> bool:
        if len(self._board._players_list) < self._board.min_players:
            self._send_to_ui("Not enough players to start the game.")
            return False

        for player in self._board._players_list:
            if not player.knows_rules:
                self._send_to_ui(f"Player {player.name} does not know the rules.")
                return False

        for item in self._board._items_list:
            if not self._board._validate_items(item):
                self._send_to_ui(f"Invalid game item: {item}.")
                return False

        self._send_to_ui("Game can be started.")
        return True

    @abstractmethod
    def is_game_over(self) -> bool: ...

    @abstractmethod
    def make_moves(self) -> None: ...

    def read_rules(self) -> None:
        print("Reading Monopoly rules...")
        for player in self._board._players_list:
            answer = input(f"{player.name}, do you want to learn the rules? (y/n): ")
            if answer.lower() in ("y", "yes"):
                player.learn_rules()

    def normalize_text(self, msg: str) -> str:
        if not isinstance(msg, str):
            raise TypeError("msg must be a string")
        return textwrap.fill(textwrap.dedent(msg), width=99999).strip()
