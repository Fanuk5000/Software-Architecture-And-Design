from typing import Any, Protocol, runtime_checkable
from random import randint


@runtime_checkable
class IGameComponent(Protocol):
    item_name: str


class Dice(IGameComponent):
    def __init__(self) -> None:
        self.item_name: str = self.__class__.__name__

    def roll_dice(self) -> Any:
        return randint(1, 6)


class Chip(IGameComponent):
    def __init__(self, item_name: str | None = None) -> None:
        self.item_name: str = item_name if item_name is not None else self.__class__.__name__
        self.chip_position: int = 0

    def move_chip(self, steps: int = 1) -> None:
        self.chip_position += steps


class Card(IGameComponent):
    def __init__(self, item_name: str | None = None) -> None:
        self.item_name: str = item_name if item_name is not None else self.__class__.__name__

    def draw_card(self) -> str:
        return "You drew a card!"
