def monopoly_sample() -> None:
    from Entities.game_components import Dice, Chip, Card

    from Entities.board_game import GameContext, MonopolyBoard
    from Entities.player import MonopolyPlayer
    from GameLogics.monopoly import MonopolyGameLogic

    # Create game context
    chip_car = Chip("Car")
    chip_hat = Chip("Hat")
    game_context = GameContext(
        min_players=2,
        max_players=4,
        players=[
            MonopolyPlayer("Alice", "Smith", chip_car),
            MonopolyPlayer("Bob", "Johnson", chip_hat)
        ],
        items=[Dice(), Card(), chip_car, chip_hat]
    )
    # Initialize game
    monopoly_board = MonopolyBoard(game_context)
    game_logic = MonopolyGameLogic(monopoly_board)

    # Read rules
    game_logic.read_rules()

    # Start game
    game_starter = game_logic.can_start_game()
    print(game_starter)
    if game_starter == "Game can be started.":
        while not game_logic.check_game_over():
            moves = game_logic.make_moves()
            for player, actions in moves.items():
                print(f"{player.name}{', '.join(actions)}")
        print("Game over!")

def mafia_sample() -> None:
    from Entities.game_components import Card
    from Entities.board_game import GameContext, MafiaBoard
    from Entities.player import MafiaPlayer
    from GameLogics.mafia import MafiaGameLogic
    # Create game context
    game_context = GameContext(
        min_players=4,
        max_players=10,
        players=[
            MafiaPlayer("Alice", "Smith", Card()),
            MafiaPlayer("Bob", "Johnson", Card()),
            MafiaPlayer("Charlie", "Brown", Card()),
            MafiaPlayer("Diana", "Prince", Card())
        ],
        items=[Card()]
    )
    # Initialize game
    mafia_board = MafiaBoard(game_context)
    game_logic = MafiaGameLogic(mafia_board)
    # Read rules
    game_logic.read_rules()
    # Give roles
    game_logic.give_roles()
    # Start game
    game_starter = game_logic.can_start_game()
    print(game_starter)
    if game_starter == "Game can be started.":
        moves = game_logic.make_moves()
        for move in moves:
            print(move)
if __name__ == "__main__":
    mafia_sample()
    # monopoly_sample()
