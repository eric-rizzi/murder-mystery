import random

from murder.config import (
    END_TIME,
    MURDER_COOL_DOWN,
    NUM_PLAYERS,
    START_TIME,
    TIME_MINUTE_INCREMENTS,
)
from murder.item import Item
from murder.person import Person
from murder.room import Room
from murder.utils import Coordinates, clear_screen, hash, wait


class Mansion:
    """
    This is where the game takes place, both in the story and in the code.

    A group of mysterious strangers have been invited to a dinner party,
    at a mansion in a secluded part of town, for an unknown reason.
    Little do they know, they may not all survive until dessert.

    You will have to investigate the mansion in different rooms throughout
    the night, to answer questions about the events which take place.

    Just be sure to stay away from the champagne, I heard it's to die for...

    ~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~

    This class simulates a generic version of a Murder Mystery board game.

    Use breakpoints, code modifications, added print statements, and more
    debugging techniques to solve the mystery, and close the case.
    """

    def __init__(self, login_id: str, *, show_intro=False) -> None:
        """
        Mansion constructor which sets random seed based on login_id

        Time starts at 0, representing minutes passed since "start" hour attribute

        :param login_id: The login_id to use for random seeding
        :param show_intro: If True, show the intro screen (takes time)
        """
        # Time starts at 0 minutes past starting time, moves in +5 (min) increments
        self.time_val = 0
        # Game start at 6pm and ends at "end" pm. "end" should be > "start"
        self.start = START_TIME
        self.end = END_TIME
        # The murderer has to wait 5 turns to attack initially
        self.cool_down = MURDER_COOL_DOWN
        # Set custom login_id seed for game
        random.seed(hash(login_id))

        # Generate rooms, players, items
        self.players = self.generate_players()  # Generate players, choose murderer
        self.room_map = self.generate_rooms()  # Generate mansion size, rooms, items, and starting location
        self.total_items = (len(self.room_map) * len(self.room_map[0])) // 2
        if self.total_items < 5:
            self.total_items = 5
        self.items: list[Item] = self.spawn_items()

        # Print intro and lore
        if show_intro:
            self.print_intro(self.players)

    @staticmethod
    def print_intro(players: list[Person]) -> None:
        """
        Intro text generator. Reads from "Intro.in" file.

        :param players: List of players to introduce
        """
        with open("res/Intro.in", "r") as file:
            clear_screen()

            lines = int(file.readline().rstrip())  # Number of lines for first paragraph
            for _ in range(lines):  # Read and print lines adding pauses in between
                print(file.readline().rstrip())
                wait_time = int(file.readline().rstrip())
                wait(wait_time)

            clear_screen()

            lines_in_cloud = int(file.readline().rstrip())
            lines_in_lightning = int(file.readline().rstrip())

            for _ in range(lines_in_cloud):  # Print cloud (all at once)
                print(file.readline().rstrip())

            for line in range(lines_in_lightning):  # Animate lightning by printing with pauses
                if line == 0:
                    wait(800)
                elif line < lines_in_lightning - 1:
                    wait(30)
                else:
                    wait(100)  # After done fully printing, wait longer

                print(file.readline().rstrip())

            title_screen_lines = int(file.readline().rstrip())
            for _ in range(title_screen_lines):
                print(file.readline().rstrip())

            wait(3500)
            clear_screen()

            intro_text = int(file.readline().rstrip())
            for _ in range(intro_text):
                print(file.readline().rstrip() + "\n")
                wait(2500)

            wait(1500)
            for p in range(len(players)):
                if p % 2 != 0 or p == 1:
                    print("\t\t" + players[p].get_name())
                    wait(1200)
                else:
                    print(players[p].get_name())
                    wait(1200)

    def time(self) -> int:
        """
        :returns: The time value
        """
        return self.time_val

    def get_rooms(self) -> list[list[Room]]:
        """
        :returns: 2d array of rooms
        """
        return self.room_map

    def get_players(self) -> list[Person]:
        """
        :returns: Array of person objects (players)
        """
        return self.players

    def get_items(self) -> list[Item]:
        """
        :returns: Array of item objects spawned in mansion
        """
        return self.items

    def alive_players(self) -> int:
        """
        :returns: Count of number of alive people
        """
        alive = 0
        for player in self.players:
            if player.is_alive():
                alive += 1
        return alive

    def get_start_and_end_times(self) -> tuple[int, int]:
        """
        :returns: [start time, end time]
        """
        return (self.start, self.end)

    def next_turn(self) -> bool:
        """
        This is the method used to run the game, turn by turn

        Completes one turn of the simulation (5 in-game minutes)
        Gives each player a chance to move/act, ending with the murderer

        :returns: True if the game is not over after the turn
        """
        # If everyone except the murderer is dead, the game ends
        if self.murderer_wins():
            self.end = self.time_val
            return False

        # Each player gets a turn, ending with the murderer
        for i in range(len(self.players)):
            # Grab current player and their location
            player = self.players[(i + self.murderer + 1) % len(self.players)]
            player_item = player.get_holds()

            # Skip dead players
            if not player.is_alive():
                continue

            # Set movement based on dice roll
            player.set_moves(random.randint(3, 7))

            # Each player gets to try to move twice
            for tried in range(2):
                if player.get_moves() <= 0:
                    break

                # People in current room
                x, y = player.get_location()
                people_in_room = self.room_map[x][y].get_people()
                # Door weights
                weights = self.room_map[x][y].get_door_weights()
                # Door costs
                costs = self.room_map[x][y].get_door_costs()
                # Door position
                dim = (len(self.room_map), len(self.room_map[0]))

                # LOGIC FOR MURDERER KILLING/MOVING
                if player.is_murderer():
                    # If the murderer is alone with someone
                    # And the murderer has an item (potential weapons)
                    # And player.attack() returns true (the murderer is not on cool_down)
                    # If the murderer is on cool_down, they have a 1/100 chance to ignore it and
                    # attack anyway
                    murderer_alone_with_player = bool(self.room_map[x][y].alive_people() == 2)
                    murderer_should_attack = (
                        player.attack(self.time_val, self.cool_down, random.randint(0, 99) == 0)
                        and player_item
                        and not player_item.is_marked()
                    )

                    if murderer_alone_with_player and murderer_should_attack:
                        # find the other alive person and kill them
                        for p in people_in_room:
                            if p.get_name() != player.get_name() and p.is_alive():
                                # Mark victim as dead
                                p.kill()
                                # Mark the item used in the murder
                                if player_item:
                                    player_item.set_marked(True)

                                # Set the murderer's new random cool_down
                                self.cool_down = self.time_val + (random.randint(1, 3) * 5)  # Update cool_down

                    # After possibly committing murder, move like a normal player.
                    # If did not commit murder, then pursue the closest player.

                    # Remove murderer from room in preparation to move
                    self.room_map[player.get_location()[0]][player.get_location()[1]].remove_player(player.get_name())
                    # If on cool_down, act like a normal player
                    if self.cool_down > self.time_val:
                        destination_room = player.choose_door(weights, costs, player.get_location(), dim)
                        tried += 1
                    # If not on cool_down, pursue closest alive player
                    else:
                        destination_room = player.pursue(player.get_location(), self.players)
                        tried += 1
                # If it's not the murderer, move randomly
                else:
                    # Remove player from room (in preparation to move)
                    x, y = player.get_location()
                    self.room_map[x][y].remove_player(player.get_name())
                    # Calculate new coordinates of player
                    destination_room = player.choose_door(weights, costs, Coordinates(x, y), dim)
                    tried += 1

                # Move player
                player.set_location(
                    destination_room[0], destination_room[1]
                )  # Move player by changing location attribute
                self.room_map[destination_room[0]][destination_room[1]].add_player(player)  # Add player to new room

            # LOGIC FOR PLAYERS PICKING UP/DROPPING ITEMS

            current_room = self.room_map[player.get_location()[0]][player.get_location()[1]]
            room_has_item = len(current_room.get_items()) > 0

            if player_item and not room_has_item:
                # If player is murderer and is holding murder weapon, drop it
                if player.is_murderer() and player_item.is_marked():
                    current_room.add_item(player.drop_item())
                # If not murderer, randomly drop item
                elif not player.is_murderer() and random.randint(0, 19) == 0:  # 1 / 20 chance
                    current_room.add_item(player.drop_item())  # currentRoom holds dropped Item
            # If player doesn't have item and room has item
            elif not player_item and room_has_item:
                if random.randint(0, 4) != 0:  # 4 / 5 chance
                    # Pick up item
                    # If item is valid and not a murder weapon, pick up
                    if current_room.get_items()[0] is not None and not current_room.get_items()[0].is_marked():
                        player.pick_up_item(current_room.get_items().pop(0))  # player holds Item
                    # Put item back if it's marked
            # If player has item and room has item
            elif player_item and room_has_item:
                # If the player is murderer and is holding a murder weapon
                if player.is_murderer() and player_item.is_marked():
                    # If the room's item is not a murder weapon
                    if not current_room.get_items()[0].is_marked():
                        # Drop the murder weapons
                        current_room.add_item(player.drop_item())
                        # Pick up the fresh item
                        player.pick_up_item(current_room.get_items().pop(0))
                # Else if the player is not the murderer and a coin flip
                elif not player.is_murderer() and random.randint(0, 1) == 0:  # 1 / 2 chance
                    # If items are valid and the room's item isn't a murder weapon
                    if (
                        current_room.get_items()[0] is not None
                        and player.get_item_name() is not None
                        and not current_room.get_items()[0].is_marked()
                    ):
                        # Player and room swap item
                        picked_up_item = current_room.get_items().pop(0)
                        dropped_item = player.drop_item()
                        player.pick_up_item(picked_up_item)
                        current_room.add_item(dropped_item)

        self.time_val += TIME_MINUTE_INCREMENTS
        return self.time_val < ((self.end - self.start) * 60)

    def generate_players(self) -> list[Person]:
        """
        Populates players[] array of Person objects

        Reads in all people from People.in, and randomly selects 5-9 of them
        to be players in the game.

        Randomly chooses one of the people to be the murderer

        :returns: Array of Person objects who are the players of the game
        """
        with open("res/People.in", "r") as file:
            total_available_people = int(file.readline().strip())  # Number of people contained in People.in

            cast_of_players: list[Person] = []

            people_to_choose_from = []  # Holds all potential people
            for i in range(total_available_people):  # Reads in all potential people
                to_add = Person(file.readline().strip())
                people_to_choose_from.append(to_add)

            taken: list[int] = []
            p = 0
            while p < NUM_PLAYERS:  # Loop to choose each character
                chosen_person = random.randint(0, total_available_people - 1)  # Choose a character from list
                if chosen_person in taken or (p % 2 == 0 and chosen_person % 2 != 0):
                    continue
                taken.append(chosen_person)
                person = people_to_choose_from[chosen_person]
                cast_of_players.append(person)  # Remove chosen character from list and add to game
                p += 1

            self.murderer = random.randint(0, len(cast_of_players) - 1)  # choose index in players[] to be the murderer
            cast_of_players[self.murderer].set_murderer(True)

            return cast_of_players

    def generate_rooms(self) -> list[list[Room]]:
        """
        Generates randomly the room_map array of rooms representing the mansion

        Creates a mansion (Room[][]) between 4x3 and 6x4 (12-24 rooms)

        Reads in all potential rooms, and populates the mansion randomly from them.
        While doing so, randomly populates some rooms with their item.

        Selects one room on an edge of the array to be the starting point
        ("The Foyer"), and places all players inside that room.

        :returns: 2D array representing rooms containing items/people
        """
        with open("res/Rooms.in", "r") as file:
            potential_rooms = int(file.readline().strip())  # Total rooms to choose from (minus starting room)

            # Generate Mansion size
            mansion_width = random.randint(4, 6)
            mansion_height = random.randint(3, 4)

            # Read rooms into a temp array, to randomly choose from
            # Room input file format is: 1 line with #ofRooms, then 3 lines per room
            # One line with name, one line with 4 doubles for weights, one line with 4 ints for costs
            rooms_to_choose_from: list[Room] = []
            for _ in range(potential_rooms):  # Read in all potential rooms, including name, weights, cost
                name = file.readline().strip()
                door_weights = list(map(float, file.readline().strip().split()))
                costs = list(map(int, file.readline().strip().split()))
                to_add = Room(name, door_weights, costs)
                rooms_to_choose_from.append(to_add)

            # Populates board with random rooms from potential rooms
            mansion: list[list[Room]] = []
            for x in range(mansion_width):
                mansion_row: list[Room] = []
                for y in range(mansion_height):
                    chosen_room = random.randint(0, len(rooms_to_choose_from) - 1)
                    mansion_row.append(rooms_to_choose_from.pop(chosen_room))
                mansion.append(mansion_row)

            # Logic for placing starting room, always at one of the four edges of the grid
            # Decide which edge (N, S, E, W)
            side_of_board = random.randint(0, 3)

            starting_weights = [0.25, 0.25, 0.25, 0.25]
            starting_costs = [3, 3, 3, 3]

            if side_of_board == 0:  # North
                x = 0  # Top edge
                y = random.randint(0, mansion_height - 1)  # Any spot
                mansion[x][y] = Room("The Foyer", starting_weights, starting_costs)
            elif side_of_board == 1:  # South
                x = mansion_width - 1  # Bottom edge
                y = random.randint(0, mansion_height - 1)  # Any spot
                mansion[x][y] = Room("The Foyer", starting_weights, starting_costs)
            elif side_of_board == 2:  # East
                x = random.randint(0, mansion_width - 1)  # Any spot
                y = mansion_height - 1  # Right edge
                mansion[x][y] = Room("The Foyer", starting_weights, starting_costs)
            else:  # West
                x = random.randint(0, mansion_width - 1)  # Any spot
                y = 0  # Left edge
                mansion[x][y] = Room("The Foyer", starting_weights, starting_costs)

            # Add players into starting room (The Foyer)
            for p in range(len(self.players)):
                self.players[p].set_location(x, y)
                mansion[x][y].add_player(self.players[p])

            return mansion

    def spawn_items(self) -> list[Item]:
        """
        Randomly spawns items throughout the mansion

        Reads in room, item pairs and then iterates through rooms
        in the mansion. If we should spawn an item in that room
        then remove the item from the dict and place it in the room

        :returns: List of created items
        """
        with open("res/Items.in", "r") as file:
            number_of_items = int(file.readline().strip())  # Reads the number of Items

            location_to_item_map: dict[str, Item] = {}

            for _ in range(number_of_items):
                item_name = file.readline().strip()
                item_location = file.readline().strip()

                item = Item(item_name)  # Create new Item with its room name
                item.set_location(item_location)
                location_to_item_map[item_location] = item  # Store in the hashmap

            items: list[Item] = []
            for x in range(len(self.room_map)):
                for y in range(len(self.room_map[x])):
                    if len(items) > self.total_items:
                        break
                    current_room = self.room_map[x][y]
                    # No item spawns in The Foyer
                    if current_room.get_room_name() == "The Foyer":
                        continue
                    # If the current room doesn't have an item
                    elif len(current_room.get_items()) == 0 and self.place_item_in_room(x, y):
                        item = location_to_item_map.pop(current_room.get_room_name(), None)  # Get item from dict
                        if item is None:
                            continue
                        current_room.add_item(item)  # Add item to room
                        items.append(item)

            # The murderer starts with the revolver. DO NOT COUNT THIS AS AN ITEM PICKUP.
            revolver = Item("Revolver")
            self.players[self.murderer].pick_up_item(revolver)
            items.append(revolver)

            return items

    def place_item_in_room(self, x: int, y: int) -> bool:
        """
        Helper for spawn_items()
        Checks the 4 neighboring rooms for items, and none exist
        flips a coin to decide whether to place an item

        :param x: The room to check is room_map[x][y]
        :param y: The room to check is room_map[x][y]
        :returns: True if we can and should place an item, false if not
        """
        # Check surrounding 4 rooms for items
        surround = 0  # True if there's an item in a bordering room
        x_arr = [-1, 0, 1, 0]
        y_arr = [0, -1, 0, 1]

        for i in range(4):
            # Cannot be out of bounds (x and y)
            if 0 <= (x + x_arr[i]) < len(self.room_map) and 0 <= (y + y_arr[i]) < len(self.room_map[0]):
                if not ((x + x_arr[i]) == x and (y + y_arr[i]) == y):
                    surrounding_room = self.room_map[(x + x_arr[i])][y + y_arr[i]]
                    if surrounding_room.get_items() and len(surrounding_room.get_items()) > 0:
                        surround += 1

        return random.randint(0, 2) != 0 and surround < 2

    def murderer_wins(self) -> bool:
        """
        :returns: True if the murderer is the last alive
        """
        return self.alive_players() == 1 and self.players[self.murderer].is_alive()
