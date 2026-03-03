from typing import TYPE_CHECKING

from GameLogics.helpers.factories import (
    AliasGameFactory,
    MafiaGameFactory,
    MonopolyGameFactory,
)
from GameLogics.mafia import MafiaLogic

if TYPE_CHECKING:
    from GameLogics.general import GameLogic
    from GameLogics.helpers.factories import GameFactory


class MenuEngine:
    def __init__(self) -> None:
        self.__options = {
            "1": ("Play Mafia", lambda: MafiaGameFactory()),
            "2": ("Play Monopoly", lambda: MonopolyGameFactory()),
            "3": ("Play Alias", lambda: AliasGameFactory()),
            "4": ("Exit", None),
        }

    def __display_game_message(self, message, end) -> None:
        print(message, end=end)

    def __display_menu(self) -> None:
        print("Welcome to the Game Menu!")
        for key, description in self.__options.items():
            print(f"{key}. {description[0]}")

    def __create_env(self, factory: "GameFactory") -> "GameLogic":
        game_context = factory.create_context()
        board = factory.create_board(game_context)
        game_logic = factory.create_logic(board)
        return game_logic

    def run(self) -> None:
        while True:
            self.__display_menu()

            choice = input("Please select an option: ")
            action = self.__options.get(choice)
            if not action:
                print("Invalid option. Please try again.")
                continue

            if action[0] == "Exit":
                self.exit_menu()
            else:
                try:
                    game_logic = self.__create_env(action[1]())
                except (ValueError, TypeError) as e:
                    print(f"Problems in game configuration {e}, try again")
                    continue
                print(f"Starting game: {action[0].split()[1]}")
                # here we subscribe the menu's display_game_message method to the game_notification event of the game logic
                game_logic.game_notification += self.__display_game_message

                game_logic.read_rules()

                if isinstance(game_logic, MafiaLogic):
                    game_logic.give_roles()

                if game_logic.can_start_game():
                    while not game_logic.is_game_over():
                        game_logic.make_moves()
                    game_logic.game_notification -= self.__display_game_message
                    print("Game over!")

    def exit_menu(self) -> None:
        print("Exiting the menu. Goodbye!")
        exit(0)
