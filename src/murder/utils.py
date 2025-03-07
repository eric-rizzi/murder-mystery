import os
import time
import typing


class Coordinates(typing.NamedTuple):
    x: int
    y: int


def valid_login_id(login_id: str) -> bool:
    """
    This method can be used to limit login_id types.
    It accepts all login IDs by default.

    :returns: True if valid, False otherwise
    """
    return True


def hash(login_id: str) -> int:
    """
    Takes a login_id and turns it into a value which can be used
    to seed the random module

    :param login_id: a valid login_id
    :returns: an integer value seed
    """
    # If no login_id was read, or login_id is incorrect length
    if not valid_login_id(login_id):
        return 1

    seed = ""
    for i in range(len(login_id)):  # Concatenates the ascii value of each login_id char to a string
        ascii_val = ord(login_id[i])
        seed += str(ascii_val)

    if len(seed) > 18:
        seed = seed[: len(seed) - 18]

    seed_val = int(seed)  # Parses string to int and returns
    return seed_val


def wait(milli: int) -> None:
    """
    Sleep method

    :param milli: milliseconds to sleep
    """
    try:
        time.sleep(milli / 1000)
    except Exception as e:
        print(e)


def clear_screen():
    """
    Clears terminal
    """
    os.system("cls" if os.name == "nt" else "clear")
