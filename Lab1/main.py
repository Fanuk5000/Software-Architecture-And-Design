from UI.menu import ui_callback


def monopoly_sample() -> None:
    from Entities.game_components import Dice, Chip, Card

    from Entities.monopoly_board import GameContext, MonopolyBoard
    from Entities.player import MonopolyPlayer
    from GameLogics.monopoly import MonopolyLogic

    # Create game context
    chip_car = Chip("Car")
    chip_hat = Chip("Hat")
    game_context = GameContext(
        min_players=2,
        max_players=4,
        players=[
            MonopolyPlayer("Alice", "Smith", chip_car),
            MonopolyPlayer("Bob", "Johnson", chip_hat),
        ],
        items=[Dice(), Card(), chip_car, chip_hat],
    )
    # Initialize game
    monopoly_board = MonopolyBoard(game_context)
    game_logic = MonopolyLogic(monopoly_board, ui_callback)
    # Read rules
    game_logic.read_rules()

    # Start game
    if game_logic.can_start_game() is True:
        while not game_logic.is_game_over():
            game_logic.make_moves()
        print("Game over!")


def mafia_sample() -> None:
    from Entities.game_components import Card
    from Lab1.Entities.mafia_board import GameContext, MafiaBoard
    from Entities.player import MafiaPlayer
    from GameLogics.mafia import MafiaLogic

    # Create game context
    game_context = GameContext(
        min_players=3,
        max_players=10,
        players=[
            MafiaPlayer("Alice", "Smith", Card()),
            MafiaPlayer("Bob", "Johnson", Card()),
            MafiaPlayer("Charlie", "Brown", Card()),
        ],
        items=[Card()],
    )
    # Initialize game
    mafia_board = MafiaBoard(game_context)
    game_logic = MafiaLogic(mafia_board, ui_callback)
    # Read rules
    game_logic.read_rules()
    # Give roles
    game_logic.give_roles()
    # Start game
    if game_logic.can_start_game() is True:
        while not game_logic.is_game_over():
            game_logic.make_moves()
        print("Game over!")


if __name__ == "__main__":
    mafia_sample()
    # monopoly_sample()
