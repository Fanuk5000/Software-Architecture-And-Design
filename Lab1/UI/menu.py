from typing import Any, Callable, TYPE_CHECKING

from GameLogics.factories import GameContextFactory, BoardFactory, LogicsFactory
from GameLogics.mafia import MafiaLogic

if TYPE_CHECKING:
    from GameLogics.general import GameLogic


def ui_callback(message: str, end: str = "\n") -> None:
    print(message, end=end)


class MenuEngine:
    def __init__(self) -> None:
        self.__options = {
            "1": "Play Mafia",
            "2": "Play Monopoly",
            "3": "Play Alias",
            "4": "Exit",
        }

    def __display_menu(self) -> None:
        print("Welcome to the Game Menu!")
        for key, description in self.__options.items():
            print(f"{key}. {description}")

    def __create_env(self, choice: str) -> "GameLogic":
        game_context = GameContextFactory.get_game_context(choice)
        board = BoardFactory.get_board(choice, game_context)
        game_logic = LogicsFactory.get_logic(choice, board, ui_callback)
        return game_logic

    def run(self) -> None:
        while True:
            self.__display_menu()
            choice = input("Please select an option: ")
            action = self.__options.get(choice)
            if not action:
                print("Invalid option. Please try again.")
                continue

            if action == "Exit":
                self.__exit_menu()
            else:
                game_logic = self.__create_env(choice)
                ui_callback(f"Starting game: {action}")

                game_logic.read_rules()

                if isinstance(game_logic, MafiaLogic):
                    game_logic.give_roles()

                if game_logic.can_start_game():
                    while not game_logic.is_game_over():
                        game_logic.make_moves()
                    ui_callback("Game over!")

    def __exit_menu(self) -> None:
        print("Exiting the menu. Goodbye!")
        exit(0)
