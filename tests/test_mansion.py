from murder.mansion import Mansion


def test_mansion_init_1():
    m = Mansion("100")

    assert m.start == 6
    assert m.end == 11
    assert m.cool_down == 25

    player_names = [p.name for p in m.players]
    assert player_names == ["Sir Brunette", "Sir Ube", "Chef Grey", "Mr. Brown", "Monsieur Verde", "Professor Purple"]

    assert len(m.room_map) == 6
    assert len(m.room_map[0]) == 4

    item_names = [i.item_name for i in m.items]
    assert len(item_names) == 14
    assert item_names == [
        "Old Sword",
        "Poison",
        "Knife",
        "Lead Pipe",
        "Scalpel",
        "Frying Pan",
        "Wrench",
        "Pool Net",
        "Tuning Fork",
        "Paper Cutter",
        "Corkscrew",
        "Fire Poker",
        "Heavy Book",
        "Revolver",
    ]

    assert m.alive_players() == 6


def test_mansion_init_2():
    """
    Make sure different random seed leads to different starting condition
    """
    m = Mansion("99")

    assert m.start == 6
    assert m.end == 11
    assert m.cool_down == 25

    player_names = [p.name for p in m.players]
    assert player_names == [
        "Reverend Amethyst",
        "Chef Grey",
        "Sir Ube",
        "Sir Brunette",
        "Monsieur Verde",
        "Solicitor Azure",
    ]

    assert len(m.room_map) == 6
    assert len(m.room_map[0]) == 4

    item_names = [i.item_name for i in m.items]
    assert len(item_names) == 13
    print(item_names)
    assert item_names == [
        "Wrench",
        "Heavy Book",
        "Rolling Pin",
        "Lead Pipe",
        "Fire Poker",
        "Candelabra",
        "Knife",
        "Tuning Fork",
        "Frying Pan",
        "Curtain Rod",
        "Pillow",
        "Piano Wire",
        "Revolver",
    ]

    assert m.alive_players() == 6


def test_mansion_next_turn_1():
    """
    Make sure game with seed 100 plays out to same end point
    """
    m = Mansion("100")

    while m.next_turn():
        pass

    assert m.alive_players() == 1
    assert m.time_val == 285

    assert m.murderer == 4

    murderer_room = m.room_map[1][1]
    assert murderer_room.get_room_name() == "Dining Room"

    murderer_room = murderer_room.get_people()
    assert len(murderer_room) == 1
    murderer = murderer_room[0]
    assert murderer.name == "Monsieur Verde"
    assert murderer.is_murderer() == True
    assert murderer.has_item() == True
    assert murderer.get_item_name() == "Knife"


def test_mansion_next_turn_2():
    """
    Make sure game with seed 99 plays out to same endpoint
    """
    m = Mansion("99")

    while m.next_turn():
        pass

    assert m.alive_players() == 1
    assert m.time_val == 120

    murderer_room = m.room_map[4][0]
    assert murderer_room.get_room_name() == "Guest Bedroom"

    murderer_room = murderer_room.get_people()
    assert len(murderer_room) == 1
    murderer = murderer_room[0]
    assert murderer.name == "Sir Brunette"
    assert murderer.is_murderer() == True
    assert murderer.has_item() == False
    assert murderer.get_item_name() == None
