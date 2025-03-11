import random
import typing

from murder.mansion import Mansion
from murder.utils import clear_screen


class SeedQuestion(typing.NamedTuple):
    t_0: str
    t_1: str
    t_2: str


def get_random_question_seeds(mansion: Mansion, num_seed_q: int) -> list[SeedQuestion]:
    """
    Reads in random question seeds from the questions input file
    Then selects a random subset of those and returns them

    Random question seeds are stored as 3 string tokens, which are
    keywords and parsing to form different questions.

    Parses the random selection for game specific attributes
    like item names, times, players, etc.

    :param num_seed_q: Number of seed questions to generate
    :returns: A 2D String array, where each row is a question, and
        each of 3 columns is a component of the question
    """
    with open("res/Questions.in", "r") as file:
        # Skip the set questions (read in driver)
        skip = int(file.readline().strip())
        for _ in range(skip):
            file.readline()

        # Read in random question pool size
        random_question_count = int(file.readline().strip())
        # Create 2D strs array to hold question parts
        question_list: list[SeedQuestion] = []

        # Store each question in a row of the list, parse the string based on ',' delimiter,
        # and store each part in a column
        for _ in range(random_question_count):
            raw_string = file.readline().strip()
            split = raw_string.split(",")
            assert len(split) == 3
            # Read in first part of question
            t_0 = split[0]

            # Add random variables to second token
            if split[1] == "ITEM":
                # Randomly select item name
                item = mansion.items[random.randint(0, len(mansion.items) - 1)]
                tried = len(mansion.items) * 2
                while item.get_item_name() == item.get_location() and tried > 0:
                    item = mansion.items[random.randint(0, len(mansion.items) - 1)]
                    tried -= 1
                t_1 = "the " + mansion.items[random.randint(0, len(mansion.items) - 1)].get_item_name()
            elif split[1] == "TIME":
                t_1 = str(random.randint(0, (mansion.time() // 5) + 1) * 5)
            else:
                # Randomly select player name
                player = mansion.players[random.randint(0, len(mansion.players) - 1)]
                n = 0
                while player.is_alive() and n < 12:
                    player = mansion.players[random.randint(0, len(mansion.players) - 1)]
                    n += 1
                t_1 = player.get_name()

            # Add random variables to third token
            if split[2] == "TIME":
                t_2 = str(random.randint(0, (mansion.time() // 5) + 1) * 5)
            else:
                t_2 = split[2]

            question_list.append(SeedQuestion(t_0, t_1, t_2))

        chosen_to_parse: list[SeedQuestion] = []
        for _ in range(num_seed_q):
            chosen_index = random.randint(0, len(question_list) - 1)
            chosen = question_list.pop(chosen_index)
            chosen_to_parse.append(SeedQuestion(chosen[0], chosen[1], chosen[2]))

        return chosen_to_parse


def get_source_code_questions(num_source_q: int) -> list[str]:
    """
    Gets a randomly selected list of pre-created questions about the source code

    :param num_source_q: Number of source code questions to select
    :returns: List of randomly selected pre-created questions about the source code
    """
    with open("res/Questions.in", "r") as file:
        # Skip the set questions (read in driver)
        skip = int(file.readline().strip())
        for _ in range(skip):
            file.readline()

        skip = int(file.readline().strip())  # Skip the random questions
        for _ in range(skip):
            file.readline()

        code_questions = int(file.readline().strip())
        questions = []
        for _ in range(code_questions):
            questions.append(file.readline().strip())

        chosen_questions = []
        for _ in range(num_source_q):
            chosen_index = random.randint(0, len(questions) - 1)
            chosen_questions.append(questions.pop(chosen_index))

        return chosen_questions


def ask_questions(
    mansion: Mansion,
    *,
    num_random_questions: int = 3,
    num_source_code_questions: int = 2,
) -> list[str]:
    """
    Generate and ask questions through the terminal. Questions are composed of:
    - A list of "hard coded" questions to ask every student
    - A randomly generated list of questions based on "question seeds"
    - A randomly selected list of pre-created questions about the source code

    :returns: List of user answers
    """
    # Read in non random questions
    with open("res/Questions.in", "r") as file:
        num_hard_coded_questions = int(file.readline().strip())
        hard_coded_question_pool = []
        for _ in range(num_hard_coded_questions):
            hard_coded_question_pool.append(file.readline().strip())

    question_seeds = get_random_question_seeds(mansion, num_random_questions)
    random_question_pool = generate_questions(mansion, question_seeds)
    code_question_pool = get_source_code_questions(num_source_code_questions)

    # Ask questions and record answers
    total_questions = num_random_questions + num_source_code_questions + num_hard_coded_questions
    questions: list[str] = []
    for question_num in range(total_questions):
        if question_num < num_hard_coded_questions:
            questions.append(hard_coded_question_pool[question_num])
        elif question_num < num_hard_coded_questions + num_random_questions:
            questions.append(random_question_pool[question_num - num_hard_coded_questions])
        else:
            questions.append(code_question_pool[question_num - num_hard_coded_questions - num_random_questions])

    # Ask questions and record answers
    answers: list[str] = []
    for i, question in enumerate(questions):
        print(f"Question {i + 1} / {len(questions)}")
        print(question)
        answers.append(input().strip())
        clear_screen()

    return answers


def generate_questions(mansion: Mansion, q_seeds: list[SeedQuestion]) -> list[str]:
    """
    Reads a 2D array of tokens and parses the possible combinations
    into their output strings

    Each row is 3 Strings representing the possible random questions
    The possible tokens are:
    TIME,PLAYER,DEATH,ROOM,DROP,GRAB
    The possible combinations (questions) are:
    TIME,PLAYER,DEATH - What time did PLAYER die?
    ROOM,PLAYER,DEATH - What room did PLAYER die?
    ROOM,ITEM,DROP - What room did ITEM get dropped first?
    ROOM,ITEM,GRAB - What room did ITEM get picked up last?
    TIME,ITEM,DROP - What time did ITEM get dropped last?
    TIME,ITEM,GRAB - What time did ITEM get picked up first?
    ROOM,PLAYER,TIME - What room was PLAYER in at TIME?
    PLAYER,TIME,GRAB - How many players were dead at TIME?
    PLAYER,TIME,DROP - How many players were alive at TIME?
    Random variables above like PLAYER, ITEM, and TIME are replaced by a possible
    in game answer

    :param q_seeds: List of seed data to turn into questions
    :returns: List of fully generated questions built from seeds
    """
    parsed: list[str] = []
    for seed in q_seeds:
        que = ""
        if seed[0] == "TIME" and seed[2] == "DEATH":
            que += "At what time did "
            que += seed[1]
            que += ' die? (Give your answer in XX:XXpm form, write "Alive" if they never died)'
        elif seed[0] == "TIME" and seed[2] == "DROP":
            que += "When did "
            que += seed[1]
            que += ' get dropped last? (Give your answer in XX:XXpm form, write "Untouched" if it was never dropped)'
        elif seed[0] == "TIME" and seed[2] == "GRAB":
            que += "What time did "
            que += seed[1]
            que += ' get picked up first? (Give your answer in XX:XXpm form, write "Untouched" if it was never grabbed)'
        elif seed[0] == "ROOM" and seed[2] == "DEATH":
            que += "In what room did "
            que += seed[1]
            que += ' die (Write "Alive" if they never died)?'
        elif seed[0] == "ROOM" and seed[2] == "DROP":
            que += "What room did "
            que += seed[1]
            que += ' get dropped first? (Write "Untouched" if it was never dropped)'
        elif seed[0] == "ROOM" and seed[2] == "GRAB":
            que += "Where did "
            que += seed[1]
            que += ' get picked up last? (Write "Untouched" if it was never grabbed)'
        elif seed[0] == "PLAYER" and seed[2] == "GRAB":
            que += "How many players were dead at "
            hour = mansion.get_start_and_end_times()[0] + int(seed[1]) // 60
            que += str(hour) + ":"
            minute = int(seed[1]) % 60
            if minute < 10:
                que += "0" + str(minute) + "pm?"
            else:
                que += str(minute) + "pm?"
        elif seed[0] == "PLAYER" and seed[2] == "DROP":
            que += "How many players were alive at "
            hour = mansion.get_start_and_end_times()[0] + int(seed[1]) // 60
            que += str(hour) + ":"
            minute = int(seed[1]) % 60
            if minute < 10:
                que += "0" + str(minute) + "pm?"
            else:
                que += str(minute) + "pm?"
        elif seed[0] == "ROOM":
            que += "What room was "
            que += seed[1]
            hour = mansion.get_start_and_end_times()[0] + int(seed[2]) // 60
            que += " in at " + str(hour) + ":"
            minute = int(seed[2]) % 60
            if minute < 10:
                que += "0" + str(minute) + "pm?"
            else:
                que += str(minute) + "pm?"

        parsed.append(que)

    return parsed


def write_answers(case_number: str, ans: list[str]) -> None:
    """
    Write answers to output file

    :param case_number: User's "case number" used to seed random
    :param ans: List of answers
    """
    with open("Answers.out", "w") as file:
        file.write(case_number + "\n")
        for answer in ans:
            file.write(answer + "\n")
