from typing import Any, TYPE_CHECKING
from dataclasses import dataclass, field
from abc import ABC, abstractmethod
from Entities.player import IPlayer

if TYPE_CHECKING:
    from Entities.game_components import IGameComponent


class BoardGame(ABC):
    max_players: int
    min_players: int
    _players_list: list[IPlayer | Any]
    _items_list: list["IGameComponent"]

    @property
    @abstractmethod
    def players_list(self) -> list[IPlayer | Any]:
        return self._players_list

    @players_list.setter
    @abstractmethod
    def players_list(self, value: list[IPlayer | Any]) -> None: ...

    @abstractmethod
    def _validate_items(self, component) -> bool: ...

    def add_player(self, new_player: IPlayer) -> None:
        if not isinstance(new_player, IPlayer):
            raise TypeError("Wrong obj, must be a player")

        if len(self._players_list) >= self.max_players:
            raise ValueError(f"Cannot add player: max players ({self.max_players}) reached")

        self._players_list.append(new_player)

    @abstractmethod
    def add_game_item(self, new_component: "IGameComponent") -> None: ...


@dataclass
class GameContext:
    min_players: int
    max_players: int
    players: list[IPlayer | Any] = field(default_factory=list)  # forward ref to avoid import
    items: list["IGameComponent"] = field(default_factory=list)

    def __post_init__(self) -> None:
        if self.min_players < 1:
            raise ValueError("min_players must be >= 1")
        if self.max_players < self.min_players:
            raise ValueError("max_players must be >= min_players")
