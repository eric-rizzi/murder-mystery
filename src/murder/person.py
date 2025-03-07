import random
import typing

from murder.item import Item
from murder.utils import Coordinates


class Person:
    """
    Person class which includes attributes for each player
    Attributes include name, item, alive, murderer, moves left, and current room
    Includes methods which make movement/murderer decisions
    """

    def __init__(self, name: str) -> None:
        self.name = name
        self.holds: typing.Optional[Item] = None
        self.is_murderer_flag = False
        self.is_alive_flag = True
        self.moves = 0
        self.room = Coordinates(0, 0)  # The (x,y) coordinates of the player in room_map

    def choose_door(
        self, weights: list[float], costs: list[int], coords: Coordinates, dim: tuple[int, int]
    ) -> Coordinates:
        """
        Given info about four doors (weight and cost array, plus location and bounds)
        this method chooses which one to go through randomly.

        :param weights: List[float] array of door weights
        :param costs: List[int] array of door costs
        :param coords: Starting coordinates of player
        :param dim: List[int] dimensions of the mansion
        :returns: New coordinates after (maybe) going through a door
        """
        assert len(coords) == 2
        assert len(dim) == 2

        # Holds the doors we have yet to check (0,1,2,3) == (N,S,E,W)
        doors = list(range(4))

        # While doors to try remain
        while len(doors) > 1:
            # Randomly choose one of the four doors
            chosen_door = doors.pop(random.randint(0, len(doors) - 1))
            # Decide probability we go through the door
            door_check = random.uniform(0.0, 1.0)

            # If the player is not trying to move out of bounds or through a door
            x, y = coords
            if chosen_door == 0 and x != 0 and weights[0] != 0.0:
                # If player randomly chooses the door and they can go through it
                if door_check > weights[chosen_door] and self.moves >= costs[chosen_door]:
                    # Walk through door
                    self.moves -= costs[chosen_door]
                    return Coordinates(x - 1, y)
            # If the player is trying to move out of bounds, don't let them
            elif chosen_door == 1 and x != dim[0] - 1 and weights[1] != 0.0:
                # If player randomly chooses the door and they can go through it
                if door_check > weights[chosen_door] and self.moves >= costs[chosen_door]:
                    self.moves -= costs[chosen_door]
                    return Coordinates(x + 1, y)
            # If the player is trying to move out of bounds, don't let them
            elif chosen_door == 2 and y != dim[1] - 1 and weights[2] != 0.0:
                # If player randomly chooses the door and they can go through it
                if door_check > weights[chosen_door] and self.moves >= costs[chosen_door]:
                    # Walk through door
                    self.moves -= costs[chosen_door]
                    return Coordinates(x, y + 1)
            # If the player is trying to move out of bounds, don't let them
            elif chosen_door == 3 and y != 0 and weights[3] != 0.0:
                if door_check > weights[chosen_door] and self.moves >= costs[chosen_door]:
                    # Walk through door
                    self.moves -= costs[chosen_door]
                    return Coordinates(x, y - 1)

        # If no door chosen, stay in the same room
        return coords

    def pursue(self, coords: Coordinates, players: list["Person"]) -> Coordinates:
        """
        Murderer movement method which locates the closest player and moves towards
        them. The murderer disregards door weights.

        :param coords: List[int] starting coordinates of player
        :param players: List[Person] the players in the game
        :returns: New coordinates after pursuing the closest player
        """
        # Index and distance of the chosen player to pursue
        player_index = -1
        min_distance = float("inf")

        # Check all players
        for p in range(len(players)):
            # Get player
            victim = players[p]
            # If chosen player is murderer or dead, skip
            if self.get_name() == victim.get_name() or not victim.is_alive():
                continue
            # Get location
            dest = victim.get_location()
            # Calculate distance formula, piece by piece
            x_dist = (dest[0] - self.room[0]) ** 2
            y_dist = (dest[1] - self.room[1]) ** 2
            distance = (x_dist + y_dist) ** 0.5
            # If this player is closer to the murderer than our currently chosen player
            if distance < min_distance:
                # Choose this player to pursue
                min_distance = distance
                player_index = p

        # If no players to pursue
        if player_index == -1:
            return coords

        # Return modified coords which pursues closest player
        dest = players[player_index].get_location()
        x, y = coords
        if x < dest[0]:
            return Coordinates(x + 1, y)
        elif x > dest[0]:
            return Coordinates(x - 1, y)
        elif y < dest[1]:
            return Coordinates(x, y + 1)
        elif y > dest[1]:
            return Coordinates(x, y - 1)
        return coords

    def attack(self, time: int, cool_down: int, rng: int) -> bool:
        """
        Decide whether or not to kill someone based on if not on cool_down

        RNG factor is also allowed which is decided when calling the method,
        if true, the murderer will always kill

        :param time: The current round time
        :param cool_down: The cool_down period for the attack
        :param rng: Random chance to override cool_down
        :returns: True if the attack is successful, False otherwise
        """
        if cool_down >= time and not rng:
            return False
        return True

    def kill(self) -> None:
        """
        Set the person to dead
        """
        assert self.is_alive_flag
        self.is_alive_flag = False

    def is_alive(self) -> bool:
        """
        Return True if alive
        """
        return self.is_alive_flag

    def set_location(self, x: int, y: int) -> None:
        """
        Sets the (x,y) location

        :param x: x coordinate in room_map[x,y]
        :param y: y coordinate in room_map[x,y]
        """
        self.room = Coordinates(x, y)

    def get_location(self) -> Coordinates:
        """
        :returns: Coordinates of location of person
        """
        return self.room

    def get_name(self) -> str:
        """
        :returns: Person's name
        """
        return self.name

    def set_name(self, name: str) -> None:
        """
        Set person's name
        """
        self.name = name

    def get_holds(self) -> typing.Optional[Item]:
        """
        :returns: Item object the person holds
        """
        return self.holds

    def get_item_name(self) -> typing.Optional[str]:
        """
        Item name method which safeguards against None

        :returns: String item name, None if no item
        """
        if self.holds is None:
            return None
        return self.holds.get_item_name()

    def is_murderer(self) -> bool:
        """
        :returns: True if murderer
        """
        return self.is_murderer_flag

    def set_murderer(self, is_murderer: bool) -> None:
        """
        Sets the is_murderer field

        :param is_murderer: Boolean true if murderer
        """
        self.is_murderer_flag = is_murderer

    def get_moves(self) -> int:
        """Return int number of spaces left the person can move"""
        return self.moves

    def set_moves(self, moves: int) -> None:
        """
        Sets the number of moves field

        :param moves: The number of spaces the person can now move
        """
        self.moves = moves

    def has_item(self) -> bool:
        """
        :returns: True if person is holding an item
        """
        return self.holds is not None

    def pick_up_item(self, item: Item) -> None:
        """
        Makes player pick up item

        :param item: Item to be held
        """
        self.holds = item

    def drop_item(self) -> Item:
        """
        Removes item from player possession

        :returns: Item dropped item
        """
        assert self.holds

        item = self.holds
        self.holds = None
        return item
