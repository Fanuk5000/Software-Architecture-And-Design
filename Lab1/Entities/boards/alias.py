from typing import TYPE_CHECKING, Any

from Entities.boards.board import BoardGame, IGameComponent
from Entities.game_components import Card, Chip
from Entities.player import AliasPlayer
from Entities.team import AliasTeam

if TYPE_CHECKING:
    from Entities.boards.board import GameContext


class AliasBoard(BoardGame):
    # fmt: off
    __CARD_WORDS = (
        "apple", "banana", "cat", "dog", "elephant", "flower", "guitar",
        "house", "ice cream", "jungle", "kite", "lion", "mountain", "notebook",
        "ocean", "pencil", "queen", "rainbow", "sun", "tree", "umbrella","violin",
        "whale", "xylophone", "yacht", "zebra", "airplane", "ball","car","dolphin",
        "egg", "fire","garden", "hat", "island","jacket", "key", "lamp", "moon", "nest",
        "orange", "pizza", "quilt", "robot", "star", "turtle", "volcano", "window", 
        "x-ray", "yogurt", "zoo", "astronaut", "bicycle", "camera", "diamond", "engine",
        "feather", "globe", "helicopter", "igloo", "jungle gym", "koala", "lighthouse",
        "microphone", "noodle", "octopus", "parrot", "quasar", "rocket",
    )
    # fmt: on
    __MAX_POSITION = 100

    def __init__(
        self,
        game_context: "GameContext | None" = None,
        teams: list[AliasTeam] | None = None,
    ) -> None:
        if game_context:
            if game_context.min_players < 4:
                raise ValueError("min_players must be >= 4")

            self.max_players = game_context.max_players
            self.min_players = game_context.min_players
            self._players_list: list[AliasPlayer] = game_context.players
            self._items_list = game_context.items
        else:
            self.max_players = 4
            self.min_players = 4
            self._players_list: list[AliasPlayer] = []
            self._items_list = []
        self.teams = (
            [
                AliasTeam(str(i), self.players_list[0 + i : 2 + i], Chip(str(i)))
                for i in range(0, len(self.players_list), 2)
            ]
            if teams is None
            else teams
        )

    @property
    def players_list(self) -> list[AliasPlayer]:
        return self._players_list

    @players_list.setter
    def players_list(self, value: list[AliasPlayer | Any]) -> None:
        if not isinstance(value, list):
            raise TypeError("players_list must be a list")

        if not all(isinstance(player, AliasPlayer) for player in value):
            raise TypeError("All players must be AliasPlayer instances")

        player_amount = len(value)

        if player_amount > self.max_players:
            raise ValueError(f"Cannot set players_list: max players ({self.max_players}) exceeded")

        if player_amount < self.min_players:
            raise ValueError(f"Cannot set players_list: min players ({self.min_players}) not met")

        if player_amount != len(set(value)):
            raise ValueError("Duplicate players are not allowed")

        if player_amount % 2 != 0:
            raise ValueError("Amount of players must be even for Alias")

        self._players_list = value

    @property
    def teams(self) -> list[AliasTeam]:
        return self._teams

    @teams.setter
    def teams(self, value: list[AliasTeam]) -> None:
        if not isinstance(value, list):
            raise TypeError("teams must be a list of AliasTeam instances")

        if not all(isinstance(team, AliasTeam) for team in value):
            raise TypeError("All teams must be AliasTeam instances")

        self._teams = value

    def _validate_items(self, component) -> bool:
        if not isinstance(component, (Card, Chip)):
            return False
        return True

    def add_game_item(self, new_component: IGameComponent) -> None:
        if not isinstance(new_component, IGameComponent):
            raise TypeError("Wrong obj, must be a game component")

        if not self._validate_items(new_component):
            raise ValueError("Invalid game component for Alias, must be a Card or Chip")

        if new_component in self._items_list:
            raise ValueError("This game component is already added")

        self._items_list.append(new_component)
