from typing import Callable


class Event:
    def __init__(self) -> None:
        self.__handlers: list[Callable] = []

    def __iadd__(self, new_handler: Callable) -> "Event":
        self.__handlers.append(new_handler)
        return self

    def __isub__(self, handler_to_remove: Callable) -> "Event":
        self.__handlers.remove(handler_to_remove)
        return self

    def invoke(self, message: str, end: str) -> None:
        for handler in self.__handlers:
            handler(message, end=end)
