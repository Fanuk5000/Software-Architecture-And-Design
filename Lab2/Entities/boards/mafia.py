from typing import TYPE_CHECKING, Any

from Entities.boards.board import BoardGame
from Entities.game_components import IGameComponent
from Entities.game_components import Card
from Entities.player import MafiaPlayer

if TYPE_CHECKING:
    from Entities.boards.board import GameContext


class MafiaBoard(BoardGame):
    def __init__(self, game_context: "GameContext | None" = None) -> None:
        if game_context:
            if game_context.min_players < 3:
                raise ValueError("min_players must be >= 3")

            self.max_players = game_context.max_players
            self.min_players = game_context.min_players
            self._players_list: list[MafiaPlayer] = game_context.players  # type: ignore
            self._items_list = game_context.items
        else:
            self.max_players = 4
            self.min_players = 3
            self._players_list: list[MafiaPlayer] = []
            self._items_list = []
        self.day_votes: dict[str, int] = {}
        self.night_votes: dict[str, int] = {}
        self.mafias: list[MafiaPlayer] = []

    @property
    def players_list(self) -> list[MafiaPlayer]:
        return self._players_list

    @players_list.setter
    def players_list(self, value: list[MafiaPlayer | Any]) -> None:
        if not isinstance(value, list):
            raise TypeError("players_list must be a list")

        if not all(isinstance(player, MafiaPlayer) for player in value):
            raise TypeError("All players must be MafiaPlayer instances")

        if len(value) > self.max_players:
            raise ValueError(f"Cannot set players_list: max players ({self.max_players}) exceeded")

        if len(value) < self.min_players:
            raise ValueError(f"Cannot set players_list: min players ({self.min_players}) not met")

        self._players_list = value

    def _validate_items(self, component) -> bool:
        if not isinstance(component, Card):
            return False
        return True

    def add_game_item(self, new_component: IGameComponent) -> None:
        if not isinstance(new_component, IGameComponent):
            raise TypeError("Wrong obj, must be a game component")

        if not self._validate_items(new_component):
            raise ValueError("Invalid game component for Mafia, must be a Card")

        if new_component in self._items_list:
            raise ValueError("This game component is already added")

        self._items_list.append(new_component)
