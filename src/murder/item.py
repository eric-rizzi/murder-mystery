import typing


class Item:
    """
    Item class which holds attributes of items, such as name
    if it was used as a murder weapon yet, and where it spawns
    """

    def __init__(self, item_name: str) -> None:
        self.item_name = item_name
        self.location: typing.Optional[str] = None
        self.marked = False

    def is_marked(self) -> bool:
        return self.marked

    def set_marked(self, to_mark: bool) -> None:
        self.marked = to_mark

    def get_item_name(self) -> str:
        return self.item_name

    def get_location(self) -> typing.Optional[str]:
        return self.location

    def set_location(self, location: str) -> None:
        self.location = location


if __name__ == "__main__":
    print("🔍 Hint: To start the investigation, you need to run `main.py`, not this file.")
