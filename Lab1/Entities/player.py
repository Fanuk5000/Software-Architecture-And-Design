from typing import Protocol, runtime_checkable, TYPE_CHECKING


if TYPE_CHECKING:
    from Entities.game_components import Chip, Card

@runtime_checkable
class IPlayer(Protocol):
    name: str
    surname: str
    knows_rules: bool
    chip: "Chip"

    def learn_rules(self) -> None:
        self.knows_rules = True

class MonopolyPlayer(IPlayer):
    def __init__(self, name: str, surname: str, chip: "Chip") -> None:
        self.name: str = name
        self.surname: str = surname
        self.knows_rules: bool = False
        self.chip: "Chip" = chip
        self.money: int = 640

class MafiaPlayer(IPlayer):
    def __init__(self, name: str, surname: str, card: "Card") -> None:
        self.name: str = name
        self.surname: str = surname
        self.knows_rules: bool = False
        self.card: "Card" = card