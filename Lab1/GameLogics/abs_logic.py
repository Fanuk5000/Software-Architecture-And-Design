import textwrap
from typing import (TYPE_CHECKING,
                    Any, Iterator, Protocol,
                    runtime_checkable,
                    )
from Entities.board_game import IBoardGame

if TYPE_CHECKING:
    from Entities.player import IPlayer


@runtime_checkable
class IGameLogic(Protocol):
    board: IBoardGame | Any

    def can_start_game(self) -> str:
        if len(self.board.players_list) < self.board.min_players:
            return "Not enough players to start the game."

        for player in self.board.players_list:
            if not player.knows_rules:
                return f"Player {player.name} does not know the rules."
            
        for item in self.board.items_list:
            if not self.board.validate_items(item):
                return f"Invalid game item: {type(item).__name__}."
        return "Game can be started."
    
    def check_game_over(self) -> bool: ...

    def make_moves(self) -> dict["IPlayer", str] | dict[Any, str] | Iterator: ...
    
    def read_rules(self) -> None:
        print("Reading Monopoly rules...")
        for player in self.board.players_list:
            answer = input(f"{player.name}, do you want to learn the rules? (y/n): ")
            if answer.lower() == "yes" or answer.lower() == "y":
                player.learn_rules()

    def normalize_text(self, msg: str) -> str:
        if not isinstance(msg, str):
            raise TypeError("msg must be a string")
        return textwrap.fill(textwrap.dedent(msg), width=99999).strip()
