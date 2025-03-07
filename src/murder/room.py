import typing

from murder.item import Item
from murder.person import Person


class Room:
    """
    Room class, representing a room in the mansion
    """

    def __init__(self, room_name: str, weights: list[float], costs: list[int]) -> None:
        """
        :param name: The name of the room
        :param weights: A list array of door weights (probabilities)
        :param costs: A list array of door costs (for use with dice roll)
        """
        self.room_name = room_name
        self.people: list[Person] = []
        self.items: list[Item] = []
        self.door_weights = weights
        self.door_costs = costs

    def add_item(self, item: Item) -> None:
        """
        Adds an item to the room

        :param item: The Item object to add
        """
        self.items.append(item)

    def add_player(self, player: Person) -> None:
        """
        Adds a player into a room

        :param player: The Person object to add
        """
        self.people.append(player)

    def get_people(self) -> list[Person]:
        """
        :returns: The Person list
        """
        return self.people

    def alive_people(self) -> int:
        """
        :returns: The number of alive people in a room
        """
        alive = 0
        for person in self.people:
            if person.is_alive():
                alive += 1
        return alive

    def remove_player(self, name: str) -> None:
        """
        Removes a player from a room

        :param name: The name of the player to remove
        """
        for i, person in enumerate(self.people):
            if person.get_name() == name:
                self.people.pop(i)
                return

    def get_room_name(self) -> str:
        """
        :returns: String name of the room
        """
        return self.room_name

    def set_room_name(self, room_name: str) -> None:
        """
        Set room name
        """
        self.room_name = room_name

    def get_items(self) -> list[Item]:
        """
        :returns: ist of items
        """
        return self.items

    def get_item_name(self) -> typing.Optional[str]:
        """
        Get name of first item if exists
        """
        if not self.items or self.items[0] is None:
            return None
        return self.items[0].get_item_name()

    def set_items(self, items: list[Item]) -> None:
        """
        Set items list
        """
        self.items = items

    def get_door_weights(self) -> list[float]:
        """
        :returns: door weights
        """
        return self.door_weights

    def set_door_weights(self, door_weights: list[float]):
        """
        Set door weights
        """
        self.door_weights = door_weights

    def get_door_costs(self) -> list[int]:
        """
        :returns: door costs
        """
        return self.door_costs

    def set_door_costs(self, door_costs: list[int]) -> None:
        """
        Set door costs
        """
        self.door_costs = door_costs
