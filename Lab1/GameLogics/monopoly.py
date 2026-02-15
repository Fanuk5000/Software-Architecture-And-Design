from time import sleep
from typing import Callable

from GameLogics.general import GameLogic
from Entities.boards.monopoly import MonopolyBoard
from Entities.game_components import Dice
from Entities.player import MonopolyPlayer


class MonopolyLogic(GameLogic):
    __PROPERTY_COST = 80
    __RENT = 20

    def __init__(self, board: MonopolyBoard, ui_callback: Callable[[str, str], None]) -> None:
        if not isinstance(board, MonopolyBoard):
            raise TypeError("board must be an instance of MonopolyBoard")
        self._board: MonopolyBoard = board
        self._ui_callback: Callable[[str, str], None] = ui_callback

    def is_game_over(self) -> bool:
        bankrupt_amount = 0
        winner = None
        for player in self._board._players_list:
            if player.money <= 0:
                bankrupt_amount += 1
            else:
                winner = player
        if bankrupt_amount >= len(self._board._players_list) - 1:
            if winner:
                self._send_to_ui(f"The winner is {winner.name}")
            return True
        return False

    def __pay_rent(self, player: MonopolyPlayer, owner: MonopolyPlayer) -> bool:
        if player.money >= self.__RENT:
            player.money -= self.__RENT
            owner.money += self.__RENT
            return True
        return False

    def __property_action(self, player: MonopolyPlayer, property_number: int) -> str:

        if player not in self._board.owned_properties:
            self._board.owned_properties[player] = []

        for owner, properties in self._board.owned_properties.items():
            if property_number in properties and owner != player:
                if self.__pay_rent(player, owner):
                    return self.normalize_text(
                        f"""
                       {player.name}
                        paid ${self.__RENT} rent to {owner.name} for property {property_number}."""
                    )
                return self.normalize_text(
                    f"""
                       {player.name} 
                        cannot afford to pay rent for property {property_number}."""
                )

        want_buy = input(
            self.normalize_text(
                f"""
                        {player.name}, you get onto property {property_number}.
                        Do you want to buy it for ${self.__PROPERTY_COST}? (y/n): """
            )
        )

        if want_buy.lower() not in ("y", "yes"):
            return self.normalize_text(
                f"{player.name} decided not to buy property {property_number}."
            )

        if property_number in self._board.owned_properties.get(player, []):
            return f"{player.name} already owns property {property_number}."

        if player.money > self.__PROPERTY_COST:
            player.money -= self.__PROPERTY_COST
            self._board.owned_properties[player].append(property_number)
            return self.normalize_text(
                f"""
                                {player.name} bought property
                                {property_number} for ${self.__PROPERTY_COST}."""
            )

        return self.normalize_text(
            f"""
                                {player.name} cannot 
                                afford property {property_number}."""
        )

    def make_moves(self) -> None:
        for player in self._board._players_list:
            for item in self._board._items_list:
                if isinstance(item, Dice):
                    points = item.roll_dice()
                    player.chip.move_chip(points)
                    player.chip.chip_position %= 100
                    self._send_to_ui(
                        f"[{player.chip.chip_position}] Threw a dice, and chip got moved +{points}"
                    )
                    sleep(1)
            if player.chip.chip_position % 5 == 0:
                self._send_to_ui(
                    "with property did: "
                    + self.__property_action(player, player.chip.chip_position)
                )
