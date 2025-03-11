#!/usr/bin/env python3
from murder.mansion import Mansion
from murder.questions import ask_questions, write_answers
from murder.utils import clear_screen, valid_case_number, wait


class MurderMystery:
    """
     __  __               _             __  __           _
    |  \/  |             | |           |  \/  |         | |
    | \  / |_   _ _ __ __| | ___ _ __  | \  / |_   _ ___| |_ ___ _ __ _   _
    | |\/| | | | | '__/ _` |/ _ \ '__| | |\/| | | | / __| __/ _ \ '__| | | |
    | |  | | |_| | | | (_| |  __/ |    | |  | | |_| \__ \ ||  __/ |  | |_| |
    |_|  |_|\__,_|_|  \__,_|\___|_|    |_|  |_|\__, |___/\__\___|_|   \__, |
                                                __/ |                  __/ |
    A debugger-based Mystery Solving game      |___/                  |__

    This is a driver class for the murder mystery game

    By: Colin Sullivan
    By: Steven Chen
    By: Ana Paula Centeno
    Ported to Python by: Eric Rizzi

    See the assignment description for information on running and debugging
    http://nifty.stanford.edu/2025/sullivan-chen-centeno-murder-mystery/
    """

    def __init__(self, case_number: str, show_intro: bool) -> None:
        self.mansion = Mansion(case_number, show_intro=show_intro)

    def end_game_stats(self) -> None:
        """
        Prints end game message with end time, # murdered.
        """
        print(" _____                     _____                ")
        print("|   __| ___  _____  ___   |     | _ _  ___  ___ ")
        print("|  |  || . ||     || -_|  |  |  || | || -_||  _|")
        print("|_____||__1||_|_|_||___|  |_____| \\_/ |___||_| \n")
        wait(3000)

        hrs = self.mansion.time() // 60
        mins = self.mansion.time() % 60
        print(f"The game ended at {self.mansion.get_start_and_end_times()[0] + hrs}:", end="")
        if mins < 10:
            print(f"0{mins}pm")
        else:
            print(f"{mins}pm")

        wait(2000)

        # 5 Players + A murderer
        num_starting = len(self.mansion.get_players())
        num_alive = self.mansion.alive_players()
        if num_alive > 1:
            print(f"{num_starting - num_alive} players were murdered. The murderer was caught.")
        else:
            print(f"{num_starting - num_alive} players were murdered. The murderer got away.")

        wait(3500)
        clear_screen()

    def play_game(self) -> None:
        continue_game = True
        while continue_game:
            continue_game = self.mansion.next_turn()

        clear_screen()
        self.end_game_stats()


# Run the game if this script is executed directly
if __name__ == "__main__":
    """
    Main method to run the Murder Mystery game
    """
    clear_screen()
    request = 'Please enter your "case number":'
    print(request)

    case_number = input().strip()

    # `case_number` check
    if valid_case_number(case_number):
        continue_game = True
        print("Print Intro? (y/N)")
        intro = input().strip().lower().startswith("y")

        game = MurderMystery(case_number, intro)
        game.play_game()

        write_answers(case_number, ask_questions(game.mansion))
