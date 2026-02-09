import textwrap
from typing import (TYPE_CHECKING,
                    Any, Protocol,
                    runtime_checkable,
                    )

if TYPE_CHECKING:
    from Entities.board_game import IBoardGame
    from Entities.player import MonopolyPlayer


@runtime_checkable
class IGameLogic(Protocol):
    board: Any["IBoardGame"]

    def can_start_game(self) -> str: ...
    
    def check_game_over(self) -> bool: ...

    def make_moves(self) -> dict["MonopolyPlayer", str]: ...
    
    def read_rules(self) -> None:
        print("Reading Monopoly rules...")
        for player in self.board.players_list:
            answer = input(f"{player.name}, do you want to learn the rules? (yes/no): ")
            if answer.lower() == "yes":
                player.learn_rules()

    def normalize_text(self, msg: str) -> str:
        if not isinstance(msg, str):
            raise TypeError("msg must be a string")
        return textwrap.fill(textwrap.dedent(msg), width=99999).strip()
