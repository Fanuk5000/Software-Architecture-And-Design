from time import sleep
from random import randint
from typing import Iterator

from GameLogics.abs_logic import IGameLogic
from Entities.board_game import MafiaBoard
from Entities.player import MafiaPlayer

class MafiaGameLogic(IGameLogic):
    CIVILIAN = "Civilian"
    MAFIA = "Mafia"

    def __init__(self, board: MafiaBoard) -> None:
        if not isinstance(board, MafiaBoard):
            raise TypeError("board must be an instance of MafiaBoard")
        self.board: MafiaBoard = board

    def can_start_game(self) -> str:
        if len(self.board.players_list) < self.board.min_players:
            return "Not enough players to start the game."

        for player in self.board.players_list:
            if not player.knows_rules:
                return f"Player {player.name} does not know the rules."

        for player in self.board.players_list:
            if player.card.item_name != self.CIVILIAN and player.card.item_name != self.MAFIA:
                return f"Player {player.name} has an invalid role: {player.card.item_name}."

        for item in self.board.items_list:
            if not self.board.validate_items(item):
                return f"Invalid game item: {type(item).__name__}."


        return "Game can be started."

    def give_roles(self) -> None:
        PLAYER_LIST = self.board.players_list
        PLAYER_AMOUNT = len(PLAYER_LIST)
        MAFIA_AMOUNT = PLAYER_AMOUNT // 3

        roles = [self.CIVILIAN] * (PLAYER_AMOUNT - MAFIA_AMOUNT) + [self.MAFIA] * MAFIA_AMOUNT

        for player in self.board.players_list:
            role_indx = randint(0, len(roles) - 1)
            role = roles.pop(role_indx)
            player.card.item_name = role
    
    def check_game_over(self) -> bool:
        mafia_count = sum(1 for player in self.board.players_list if player.card.item_name == self.MAFIA)
        civilian_count = sum(1 for player in self.board.players_list if player.card.item_name == self.CIVILIAN)

        if mafia_count == 0:
            print("Civilians win!")
            return True
        elif mafia_count >= civilian_count:
            print("Mafia wins!")
            return True
        return False
    
    def make_moves(self) -> dict[MafiaPlayer, str] | Iterator:
        yield self.__day_actions()
        yield ["Night actions are not implemented yet."]

    def __day_actions(self) -> dict[str, int]:
        player_list = self.board.players_list
        day_votes = self.board.day_votes

        for player_voter in player_list:
            for player in player_list:
                kicked_SN = player.name + ' ' + player.surname if player_voter != player else 'yourself'
                kick = input(
                    f"{player_voter.name} {player_voter.surname}, do you want to kick {kicked_SN} (y/n): "
                    )
                if kick.lower() == 'y' or kick.lower() == 'yes':
                    naming = f"{player.name}_{player.surname}"
                    day_votes[naming] = day_votes.get(naming, 0) + 1
                    break
        return day_votes

    def __night_actions(self) -> None:
        pass
