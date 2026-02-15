from random import choice, randint
from time import sleep
from typing import Callable

from GameLogics.general import GameLogic
from Entities.boards.alias import AliasBoard


class AliasLogic(GameLogic):
    def __init__(self, board: AliasBoard, ui_callback: Callable[[str, str], None]) -> None:
        if not isinstance(board, AliasBoard):
            raise TypeError("board must be an instance of AliasBoard")
        self._board: AliasBoard = board
        self._ui_callback: Callable[[str, str], None] = ui_callback

    def is_game_over(self) -> bool:
        for team in self._board.teams:
            if team.chip.chip_position >= 100:
                self._send_to_ui(f"The winner is team {team.name}!")
                return True
        return False

    def can_start_game(self) -> bool:
        if len(self._board.players_list) < self._board.min_players:
            self._send_to_ui("Not enough players to start the game.")
            return False

        for player in self._board.players_list:
            if not player.knows_rules:
                self._send_to_ui(f"Player {player.name} does not know the rules.")
                return False

        if len(self._board.players_list) % 2 != 0:
            self._send_to_ui("Can`t start game, the amount of players is not even")
            return False

        for item in self._board._items_list:
            if not self._board._validate_items(item):
                self._send_to_ui(f"Invalid game item: {item}.")
                return False

        self._send_to_ui("Game can be started.")
        return True

    def __generate_word(self) -> list[str]:
        words = []
        for _ in "123":
            while True:
                word = choice(self._board.__CARD_WORDS)
                if word not in words:
                    words.append(word)
                    break
        print(words)
        return words

    def make_moves(self) -> None:
        for team in self._board.teams:
            steps = 0
            for player in team.players:
                words = self.__generate_word()
                for word in words:
                    self._send_to_ui(f"{player} trying to explain what the word {word} means...")
                    sleep(0.6)
                    if randint(0, 1):
                        steps += 1
                        self._send_to_ui(f"Successfully explained it!")
                    else:
                        self._send_to_ui(f"Failed to explain it.")
            team.chip.chip_position += steps
