from time import sleep

from GameLogics.abs_logic import IGameLogic
from Entities.board_game import MonopolyBoard
from Entities.game_components import Dice
from Entities.player import MonopolyPlayer

class MonopolyGameLogic(IGameLogic):
    def __init__(self, board: MonopolyBoard) -> None:
        if not isinstance(board, MonopolyBoard):
            raise TypeError("board must be an instance of MonopolyBoard")
        self.board: MonopolyBoard = board
    

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
    
    def check_game_over(self) -> bool:
        bankrupt_amount = 0
        winner = None
        for player in self.board.players_list:
            if player.money <= 0:
                bankrupt_amount += 1
            else:
                winner = player
        if bankrupt_amount >= len(self.board.players_list) - 1:
            if winner:
                print(f"The winner is {winner.name}")
            return True
        return False

    def _property_action(self, player: MonopolyPlayer, property_number: int) -> str:
        property_cost = 80
        if player not in self.board.owned_properties:
            self.board.owned_properties[player] = []
        
        for owner, properties in self.board.owned_properties.items():
            if property_number in properties and owner != player:
                rent = 20  # Assuming a fixed rent for simplicity
                if player.money >= rent:
                    player.money -= rent
                    owner.money += rent
                    return self.normalize_text(f"""
                       {player.name}
                        paid ${rent} rent to {owner.name} for property {property_number}."""
                        )
                return self.normalize_text(f"""
                       {player.name} 
                        cannot afford to pay rent for property {property_number}."""
                        )
            
        want_buy = input(self.normalize_text(
                        f"""
                        {player.name}, you get onto property {property_number}.
                        Do you want to buy it for ${property_cost}? (yes/no): """))
        if want_buy.lower() == "yes":
            if property_number not in self.board.owned_properties[player]:
                    if player.money > property_cost:
                        player.money -= property_cost
                        self.board.owned_properties[player].append(property_number)
                        return self.normalize_text(f"""
                                            bought property
                                            {property_number} for ${property_cost}."""
                                            )
                    return self.normalize_text(f"""
                                           cannot 
                                           afford property {property_number}."""
                                           )
            else:
                return f"already owns property {property_number}."
        else:
            return f"decided not to buy property {property_number}."

    def make_moves(self) -> dict[MonopolyPlayer, str]:
        players_actions = {}

        for player in self.board.players_list:
            players_actions[player] = []
            for item in self.board.items_list:
                if isinstance(item, Dice):
                    points = item.roll_dice()
                    player.chip.move_chip(points)
                    player.chip.chip_position %= 100  # Assuming a standard Monopoly board with 100 spaces
                    players_actions[player].append(
                        f"[{player.chip.chip_position}] Threw a dice, and chip got moved +{points}")
                    sleep(1)
            if player.chip.chip_position % 5 == 0:
                players_actions[player].append("with property did: " + 
                                self._property_action(
                                    player, player.chip.chip_position))
        return players_actions
