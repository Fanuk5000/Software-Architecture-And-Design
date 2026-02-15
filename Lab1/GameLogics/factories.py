from calendar import c
from typing import Any, Callable

from GameLogics.mafia import MafiaLogic
from GameLogics.monopoly import MonopolyLogic
from GameLogics.alias import AliasLogic
from GameLogics.general import GameLogic

from Entities.boards.alias import AliasBoard
from Entities.boards.mafia import MafiaBoard
from Entities.boards.monopoly import MonopolyBoard
from Entities.boards.board import GameContext

from Entities.player import MafiaPlayer, MonopolyPlayer, AliasPlayer
from Entities.game_components import Card, Dice, Chip


class LogicsFactory:
    LOGICS = {
        "1": MafiaLogic,
        "2": MonopolyLogic,
        "3": AliasLogic,
    }

    @staticmethod
    def get_logic(choice: str, board: Any, ui_callback: Callable[[str, str], None]) -> GameLogic:
        logic_class = LogicsFactory.LOGICS.get(choice)
        if not logic_class:
            raise ValueError("Invalid choice for game logic.")
        return logic_class(board, ui_callback)


class BoardFactory:
    BOARDS = {
        "1": MafiaBoard,
        "2": MonopolyBoard,
        "3": AliasBoard,
    }

    @staticmethod
    def get_board(choice: str, game_context: Any) -> Any:
        board_class = BoardFactory.BOARDS.get(choice)
        if not board_class:
            raise ValueError("Invalid choice for game board.")
        return board_class(game_context)


class GameContextFactory:
    SETUP_GAME_CONTEXTS = {
        "1": lambda: GameContextFactory.__setup_mafia(),
        "2": lambda: GameContextFactory.__setup_monopoly(),
        "3": lambda: GameContextFactory.__setup_alias(),
    }

    @classmethod
    def __general_setup(cls) -> tuple:
        player_initials = []
        min_players = int(input("Enter minimum number of players: "))
        max_players = int(input("Enter maximum number of players: "))
        for player in range(min_players, max_players + 1):
            name = input(f"Enter name for player {player + 1}: ")
            surname = input(f"Enter surname for player {player + 1}: ")
            player_initials.append((name, surname))
        return (min_players, max_players, player_initials)

    @classmethod
    def __setup_mafia(
        cls,
    ) -> GameContext:
        min_players, max_players, player_initials = cls.__general_setup()
        players = [MafiaPlayer(name, surname, Card()) for name, surname in player_initials]
        game_context = GameContext(
            min_players=min_players,
            max_players=max_players,
            players=players,
            items=[Card()],
        )
        return game_context

    @classmethod
    def __setup_monopoly(
        cls,
    ) -> GameContext:
        min_players, max_players, player_initials = cls.__general_setup()
        players = [MonopolyPlayer(name, surname, Chip()) for name, surname in player_initials]
        game_context = GameContext(
            min_players=min_players,
            max_players=max_players,
            players=players,
            items=[Card(), Dice()],
        )
        return game_context

    @classmethod
    def __setup_alias(
        cls,
    ) -> GameContext:
        min_players, max_players, player_initials = cls.__general_setup()
        players = [AliasPlayer(name, surname, Chip()) for name, surname in player_initials]
        game_context = GameContext(
            min_players=min_players,
            max_players=max_players,
            players=players,
            items=[Card(), Dice()],
        )
        return game_context

    @classmethod
    def get_game_context(cls, choice: str) -> GameContext:
        setup_func = cls.SETUP_GAME_CONTEXTS.get(choice)
        if not setup_func:
            raise ValueError("Invalid choice for game context setup.")
        return setup_func()
