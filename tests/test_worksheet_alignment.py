import typing
from pathlib import Path

# Define the project root directory relative to this test file
# Assuming this test file is in the 'tests' directory
PROJECT_ROOT = Path(__file__).parent.parent


def get_line(file_path_relative: str, line_number: int) -> typing.Optional[str]:
    """
    Helper function to check if a specific line in a file contains the expected content.

    Args:
        file_path_relative: Path to the file relative to the project root.
        line_number: The 1-based line number to check.
        expected_content: The exact string expected on that line (leading/trailing whitespace is ignored).

    Raises:
        FileNotFoundError: If the file doesn't exist.
        IndexError: If the file doesn't have the specified line number.
        AssertionError: If the line content doesn't match the expected content.
    """
    file_path = PROJECT_ROOT / file_path_relative
    assert file_path.exists(), f"File not found: {file_path}"

    with open(file_path, "r") as f:
        lines = f.readlines()

    if len(lines) <= line_number:
        return None

    # Adjust for 0-based indexing
    actual_content = lines[line_number - 1].strip()
    return actual_content


def test_worksheet_problem_1_1():
    """
    Tests the content of line 78 in src/murder/main.py
    - Problem(s): 1.1 and 1.6
    """
    loc = get_line("src/murder/main.py", 78)
    assert loc == "request = 'Please enter your \"case number\":'"


def test_worksheet_problem_1_5():
    """
    Tests the content of line 81 in src/murder/main.py
    - Problem(s): 1.5
    """
    loc = get_line("src/murder/main.py", 81)
    assert loc == "case_number = input().strip()"


def test_worksheet_problem_2_1():
    """
    Tests the content of line 57 in src/murder/mansion.py
    - Problem(s): 2.1
    """
    loc = get_line("src/murder/mansion.py", 57)
    assert loc == "self.players = self.generate_players()  # Generate players, choose murderer"


def test_worksheet_problem_2_4():
    """
    Tests the content of line 326 in src/murder/mansion.py
    - Problem(s): 2.4
    """
    loc = get_line("src/murder/mansion.py", 326)
    assert loc == "taken: list[int] = []"


def test_worksheet_problem_2_9():
    """
    Tests the content of line 340 in src/murder/mansion.py
    - Problem(s): 2.9
    """
    loc = get_line("src/murder/mansion.py", 340)
    assert loc == "return cast_of_players"


def test_worksheet_problem_3_1():
    """
    Tests the content of line 58 in src/murder/mansion.py
    - Problem(s): 3.1
    """
    loc = get_line("src/murder/mansion.py", 58)
    assert loc == "self.room_map = self.generate_rooms()  # Generate mansion size, rooms, items, and starting location"


def test_worksheet_problem_4_1():
    """
    Tests the content of line 213 in src/murder/mansion.py
    - Problem(s): 4.1
    """
    loc = get_line("src/murder/mansion.py", 213)
    assert loc == "murderer_should_attack = ("


def test_worksheet_problem_4_2():
    """
    Tests the content of line 239 in src/murder/person.py
    - Problem(s): 4.2
    """
    loc = get_line("src/murder/person.py", 239)
    assert loc == "self.holds = item"


def test_worksheet_problem_5_5():
    """
    Tests the content of line 81 and 87 of in src/murder/main.py
    - Problem(s): 5.5
    """
    loc_1 = get_line("src/murder/main.py", 81)
    assert loc_1 == "case_number = input().strip()"

    loc_1 = get_line("src/murder/main.py", 87)
    assert loc_1 == 'intro = input().strip().lower().startswith("y")'
