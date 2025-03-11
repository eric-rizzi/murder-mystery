import os
import time
import typing


class Coordinates(typing.NamedTuple):
    x: int
    y: int


def valid_case_number(case_number: str) -> bool:
    """
    This method can be used to limit "case number" types. It accepts all case
    numbers by default.

    :returns: True if valid, False otherwise
    """
    return True


def hash(case_number: str) -> int:
    """
    Takes a "case number" and turns it into a value which can be used to seed
    the random module.

    :param case_number: A token used to seed the game
    :returns: An integer value seed
    """
    if not valid_case_number(case_number):
        return 1

    seed = ""
    for c in case_number:  # Concatenates the ascii value of each char to a string
        ascii_val = ord(c)
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
