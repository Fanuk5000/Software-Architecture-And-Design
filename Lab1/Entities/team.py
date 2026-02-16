from typing import Any, TYPE_CHECKING, Union
from abc import ABC, abstractmethod

if TYPE_CHECKING:
    from Entities.player import IPlayer, AliasPlayer
    from Entities.game_components import Chip


class Team(ABC):
    """Abstract base class defining the Team interface (players property)."""

    name: str
    _players: list[Union["IPlayer", Any]]

    @property
    @abstractmethod
    def players(self) -> list[Union["IPlayer", Any]]: ...

    @players.setter
    @abstractmethod
    def players(self, value: list[Union["IPlayer", Any]]) -> None: ...


class AliasTeam(Team):
    def __init__(self, name: str, players: list["AliasPlayer"], chip: "Chip") -> None:
        self.name: str = name
        self._players: list["AliasPlayer"] = players
        self.chip: "Chip" = chip

    @property
    def players(self) -> list["AliasPlayer"]:
        return self._players

    @players.setter
    def players(self, value: list[Union["AliasPlayer", Any]]) -> None:
        if not all(isinstance(player, AliasPlayer) for player in value):
            raise TypeError("All players must be AliasPlayer instances")

        self._players = value
