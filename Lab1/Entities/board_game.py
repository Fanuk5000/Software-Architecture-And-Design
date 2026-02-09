from typing import Protocol, runtime_checkable, TYPE_CHECKING
from dataclasses import dataclass, field

from Entities.player import MonopolyPlayer
from Entities.game_components import IGameComponent, Dice, Chip, Card


@runtime_checkable
class IBoardGame(Protocol):

    max_players: int
    min_players: int
    players_list: list[MonopolyPlayer]
    items_list: list[IGameComponent]

    def validate_items(self, component) -> bool: ...

    def add_player(self, new_player: MonopolyPlayer) -> None:
        if not isinstance(new_player, MonopolyPlayer):
            raise TypeError("Wrong obj, must be a player")
        
        if len(self.players_list) >= self.max_players:
            raise ValueError(f"Cannot add player: max players ({self.max_players}) reached")

        self.players_list.append(new_player)
    
    def add_game_item(self, new_component: IGameComponent) -> None: ...

@dataclass
class GameContext:
    min_players: int
    max_players: int
    players: list["MonopolyPlayer"] = field(default_factory=list)  # forward ref to avoid import
    items: list["IGameComponent"] = field(default_factory=list)

    def __post_init__(self) -> None:
        if self.min_players < 1:
            raise ValueError("min_players must be >= 1")
        if self.max_players < self.min_players:
            raise ValueError("max_players must be >= min_players")

class MonopolyBoard(IBoardGame):
    def __init__(self, game_context: GameContext | None = None) -> None:
        if game_context:
            if game_context.min_players < 1:
                raise ValueError("min_players must be >= 1")

            self.max_players = game_context.max_players
            self.min_players = game_context.min_players
            self.players_list = game_context.players
            self.items_list = game_context.items
        else:
            self.max_players = 4
            self.min_players = 2
            self.players_list = []
            self.items_list = []
        self.owned_properties: dict[MonopolyPlayer, list[int]] = {}

    def validate_items(self, component) -> bool:
        valid_components = (Dice, Chip)
        for valid_component in valid_components:
            if not isinstance(component, valid_component):
                return False
        return True
    
    def add_game_item(self, new_component: IGameComponent) -> None:
        if not isinstance(new_component, IGameComponent):
            raise TypeError("Wrong obj, must be a game component")
        
        if not self.validate_items(new_component):
            raise ValueError("Invalid game component for Monopoly, must be a Dice or Chip")
        
        if new_component in self.items_list:
            raise ValueError("This game component is already added")

        self.items_list.append(new_component)

class MafiaBoard(IBoardGame):
    def __init__(self, game_context: GameContext | None = None) -> None:
        if game_context:
            if game_context.min_players < 3:
                raise ValueError("min_players must be >= 3")

            self.max_players = game_context.max_players
            self.min_players = game_context.min_players
            self.players_list = game_context.players
            self.items_list = game_context.items
        else:
            self.max_players = 4
            self.min_players = 3
            self.players_list = []
            self.items_list = []
        

    def validate_items(self, component) -> bool:
        if not isinstance(component, Card):
            return False
        return True
    
    def add_game_item(self, new_component: IGameComponent) -> None:
        if not isinstance(new_component, IGameComponent):
            raise TypeError("Wrong obj, must be a game component")
        
        if not self.validate_items(new_component):
            raise ValueError("Invalid game component for Mafia, must be a Card")
        
        if new_component in self.items_list:
            raise ValueError("This game component is already added")

        self.items_list.append(new_component)