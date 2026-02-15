from typing import TYPE_CHECKING, Any

from Entities.boards.board import BoardGame
from Entities.player import MonopolyPlayer
from Entities.game_components import IGameComponent, Dice, Chip

if TYPE_CHECKING:
    from Entities.boards.board import GameContext


class MonopolyBoard(BoardGame):
    def __init__(self, game_context: "GameContext | None" = None) -> None:
        if game_context:
            if game_context.min_players < 1:
                raise ValueError("min_players must be >= 1")

            self.max_players: int = game_context.max_players
            self.min_players: int = game_context.min_players
            self._players_list: list["MonopolyPlayer"] = game_context.players
            self._items_list = game_context.items
        else:
            self.max_players = 4
            self.min_players = 2
            self._players_list: list["MonopolyPlayer"] = []
            self._items_list = []
        self.owned_properties: dict["MonopolyPlayer", list[int]] = {}

    def _validate_items(self, component) -> bool:
        if not isinstance(component, (Dice, Chip)):
            return False
        return True

    @property
    def players_list(self) -> list[MonopolyPlayer]:
        return self._players_list

    @players_list.setter
    def players_list(self, value: list[MonopolyPlayer | Any]) -> None:
        if not isinstance(value, list):
            raise TypeError("players_list must be a list")

        if not all(isinstance(player, MonopolyPlayer) for player in value):
            raise TypeError("All players must be MonopolyPlayer instances")

        if len(value) > self.max_players:
            raise ValueError(f"Cannot set players_list: max players ({self.max_players}) exceeded")

        if len(value) < self.min_players:
            raise ValueError(f"Cannot set players_list: min players ({self.min_players}) not met")

        self._players_list = value

    def add_game_item(self, new_component: IGameComponent) -> None:
        if not isinstance(new_component, IGameComponent):
            raise TypeError("Wrong obj, must be a game component")

        if not self._validate_items(new_component):
            raise ValueError("Invalid game component for Monopoly, must be a Dice or Chip")

        if new_component in self._items_list:
            raise ValueError("This game component is already added")

        self._items_list.append(new_component)
