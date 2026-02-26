from abc import ABC, abstractmethod
from typing import Any

from Entities.boards.alias import AliasBoard
from Entities.boards.board import GameContext
from Entities.boards.mafia import MafiaBoard
from Entities.boards.monopoly import MonopolyBoard
from Entities.game_components import Card, Chip, Dice
from Entities.player import AliasPlayer, MafiaPlayer, MonopolyPlayer
from GameLogics.alias import AliasLogic
from GameLogics.mafia import MafiaLogic
from GameLogics.monopoly import MonopolyLogic


class GameFactory(ABC):
    @abstractmethod
    def create_context(self) -> GameContext: ...

    @abstractmethod
    def create_board(self, game_context: GameContext) -> Any: ...

    @abstractmethod
    def create_logic(self, board: Any) -> Any: ...

    def _general_context_setup(self) -> tuple:
        player_initials = []
        min_players = int(input("Enter minimum number of players: "))
        max_players = int(input("Enter maximum number of players: "))
        for player in range(0, max_players):
            name = input(f"Enter name for player {player + 1}: ")
            surname = input(f"Enter surname for player {player + 1}: ")
            player_initials.append((name, surname))
        return (min_players, max_players, player_initials)


class MafiaGameFactory(GameFactory):
    def create_context(self) -> GameContext:
        min_players, max_players, player_initials = self._general_context_setup()
        players = [
            MafiaPlayer(name, surname, Card()) for name, surname in player_initials
        ]
        game_context = GameContext(
            min_players=min_players,
            max_players=max_players,
            players=players,
            items=[Card()],
        )
        return game_context

    def create_board(self, game_context: GameContext) -> MafiaBoard:
        if not MafiaBoard:
            raise ValueError("Invalid choice for game board.")
        return MafiaBoard(game_context)

    def create_logic(self, board: MafiaBoard) -> MafiaLogic:
        return MafiaLogic(board)


class MonopolyGameFactory(GameFactory):
    def create_context(self) -> GameContext:
        min_players, max_players, player_initials = self._general_context_setup()
        players = [
            MonopolyPlayer(name, surname, Chip()) for name, surname in player_initials
        ]
        game_context = GameContext(
            min_players=min_players,
            max_players=max_players,
            players=players,
            items=[Chip(), Dice()],
        )
        return game_context

    def create_board(self, game_context: GameContext) -> MonopolyBoard:
        if not MonopolyBoard:
            raise ValueError("Invalid choice for game board.")
        return MonopolyBoard(game_context)

    def create_logic(self, board: MonopolyBoard) -> MonopolyLogic:
        return MonopolyLogic(board)


class AliasGameFactory(GameFactory):
    def create_context(self) -> GameContext:
        min_players, max_players, player_initials = self._general_context_setup()
        players = [
            AliasPlayer(name, surname, Chip()) for name, surname in player_initials
        ]
        game_context = GameContext(
            min_players=min_players,
            max_players=max_players,
            players=players,
            items=[Card(), Chip()],
        )
        return game_context

    def create_board(self, game_context: GameContext) -> AliasBoard:
        if not AliasBoard:
            raise ValueError("Invalid choice for game board.")
        return AliasBoard(game_context)

    def create_logic(self, board: AliasBoard) -> AliasLogic:
        return AliasLogic(board)
