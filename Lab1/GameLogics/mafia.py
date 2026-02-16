from time import sleep
from random import randint
from typing import Callable

from GameLogics.general import GameLogic
from Entities.boards.mafia import MafiaBoard
from Entities.player import MafiaPlayer


class MafiaLogic(GameLogic):
    __CIVILIAN = "Civilian"
    __MAFIA = "Mafia"

    def __init__(self, board: MafiaBoard, ui_callback: Callable[[str, str], None]) -> None:
        if not isinstance(board, MafiaBoard):
            raise TypeError("board must be an instance of MafiaBoard")
        self._board: MafiaBoard = board
        self.__PLAYER_LIST: list[MafiaPlayer] = self._board._players_list
        self._ui_callback: Callable[[str, str], None] = ui_callback
        self.__end = False

    def can_start_game(self) -> bool:
        if len(self.__PLAYER_LIST) < self._board.min_players:
            self._send_to_ui("Not enough players to start the game.")
            return False

        for player in self.__PLAYER_LIST:
            if not player.knows_rules:
                self._send_to_ui(f"Player {player.name} does not know the rules.")
                return False

        for player in self.__PLAYER_LIST:
            if player.card.item_name != self.__CIVILIAN and player.card.item_name != self.__MAFIA:
                self._send_to_ui(
                    f"Player {player.name} has an invalid role: {player.card.item_name}."
                )
                return False

        for item in self._board._items_list:
            if not self._board._validate_items(item):
                self._send_to_ui(f"Invalid game item: {item}.")
                return False
        self._send_to_ui("Game can be started.")
        return True

    def give_roles(self) -> None:
        PLAYER_LIST = self.__PLAYER_LIST
        PLAYER_AMOUNT = len(PLAYER_LIST)
        MAFIA_AMOUNT = PLAYER_AMOUNT // 3

        roles = [self.__CIVILIAN] * (PLAYER_AMOUNT - MAFIA_AMOUNT) + [self.__MAFIA] * MAFIA_AMOUNT

        for player in self.__PLAYER_LIST:
            role_indx = randint(0, len(roles) - 1)
            role = roles.pop(role_indx)
            player.card.item_name = role
            if role == self.__MAFIA:
                self._board.mafias.append(player)

    def is_game_over(self) -> bool:
        sleep(1)
        if self.__end:
            return True

        mafia_count = len(self._board.mafias)
        civilian_count = sum(
            1 for player in self.__PLAYER_LIST if player.card.item_name == self.__CIVILIAN
        )

        if mafia_count == 0:
            self._send_to_ui("\nCivilians win!")
            return True
        elif mafia_count >= civilian_count:
            self._send_to_ui("\nMafia wins!")
            return True
        return False

    def make_moves(self) -> None:
        self._send_to_ui("Day phase: Players discuss and vote to kick someone out.")
        while self.__have_equals_votes(self._board.day_votes):
            self.__day_actions()
        else:
            self.__del_player(self._board.day_votes)

        if self.is_game_over():
            sleep(1)
            self.__end = True
            return

        self._send_to_ui("Night phase: Mafia members choose someone to kill.")
        while self.__have_equals_votes(self._board.night_votes):
            self.__night_actions()
        else:
            self.__del_player(self._board.night_votes)

    def __del_player(self, votes: dict[str, int]) -> None:
        max_votes_player = max(votes, key=lambda player: votes[player])
        name, surname = max_votes_player.split("_")

        if votes is self._board.day_votes:
            message = f"{name} {surname} has been kicked out by the vote."
        else:
            message = f"{name} {surname} has been killed tonight."

        for player in self.__PLAYER_LIST:
            if player.name == name and player.surname == surname:
                self.__PLAYER_LIST.remove(player)
                if player in self._board.mafias:
                    self._board.mafias.remove(player)
                self._send_to_ui(message)
                break

    def __have_equals_votes(self, votes: dict[str, int]) -> bool:
        if not votes:
            return True
        max_votes = max(votes.values())
        if list(votes.values()).count(max_votes) > 1:
            self._send_to_ui("There is a tie in votes. Revoting...")
            return True
        return False

    def __day_actions(self) -> None:
        day_votes = self._board.day_votes
        for player_voter in self.__PLAYER_LIST:
            kick = ""
            while kick.lower() not in ("y", "yes"):
                for target_player in self.__PLAYER_LIST:
                    kicked_SN = (
                        target_player.name + " " + target_player.surname
                        if player_voter != target_player
                        else "yourself"
                    )
                    kick = input(
                        f"{player_voter.name} {player_voter.surname}, do you want to kick {kicked_SN} (y/n): "
                    )
                    if kick.lower() in ("y", "yes"):
                        naming = f"{target_player.name}_{target_player.surname}"
                        day_votes[naming] = day_votes.get(naming, 0) + 1
                        break

    def __night_actions(self) -> None:
        self._send_to_ui("Night phase: Mafia members choose someone to kill.")
        for player in self._board.mafias:
            for target_player in self.__PLAYER_LIST:
                if target_player not in self._board.mafias:
                    want_kill = input(
                        f"{player.name} {player.surname}, do you want to kill {target_player.name} {target_player.surname} (y/n): "
                    )
                    if want_kill.lower() in ("y", "yes"):
                        naming = f"{target_player.name}_{target_player.surname}"
                        self._board.night_votes[naming] = self._board.night_votes.get(naming, 0) + 1
                        break
