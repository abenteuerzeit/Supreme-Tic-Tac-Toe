import os
import random
import shutil
from config import Config
from board import Board
from player import HumanPlayer, ComputerPlayer


class Game:

    def __init__(self):
        self.stats = {"wins": 0, "losses": 0, "ties": 0}
        self.settings = {
            "show_stats": True,
            "show_commands": True,
            "show_game_settings": True,
            "difficulty": 'normal'
        }
        self.human = HumanPlayer(Config.PLAYERS["HUMAN"])
        self.computer = ComputerPlayer(Config.PLAYERS["COMPUTER"],
                                       self.settings["difficulty"])
        self.board = Board()

    def clear_screen(self):
        os.system('cls' if os.name == 'nt' else 'clear')

    def reset_board(self):
        self.board.reset()
        if random.choice([True, False]):
            random_move = random.choice(self.board.get_free_fields())
            self.board.set_cell(*random_move, self.computer.symbol)

    def display_stats(self):
        if self.settings["show_stats"]:
            stats_line = self.format_stats_line()
            print(f"\033[1;32m{stats_line}\033[0m")

    def format_stats_line(self):
        terminal_width = shutil.get_terminal_size().columns
        stats_message = (f"Wins: {self.stats['wins']} | "
                         f"Losses: {self.stats['losses']} | "
                         f"Ties: {self.stats['ties']}")
        return stats_message.center(terminal_width)

    def display_title_bar(self):
        terminal_width = shutil.get_terminal_size().columns
        title = "Tic-Tac-Toe"
        difficulty_setting = f"Difficulty: {self.settings['difficulty'].capitalize()}"
        stats_setting = f"Stats: {'On' if self.settings['show_stats'] else 'Off'}"
        combined_settings = difficulty_setting + "  |  " + stats_setting
        settings_padding = (terminal_width - len(combined_settings)) // 2
        separator = "\033[1;34m" + "=" * terminal_width + "\033[0m"
        title_line = "\033[1;34m" + title.center(terminal_width) + "\033[0m"
        settings_line = (" " * settings_padding + "\033[1;34m" +
                         combined_settings + "\033[0m")

        print(title_line)
        if self.settings["show_commands"]:
            commands = "[settings] Change Settings | [help] Suggest Move"
            commands_line = "\033[1;33m" + commands.center(
                terminal_width) + "\033[0m"
            print(commands_line)
        if self.settings["show_game_settings"]:
            print(separator)
            print(settings_line)
            print(separator)

    def provide_help(self):
        suggestion = self.human.suggest_move(self.board)
        help_message_color = "\033[1;33m"
        no_move_color = "\033[1;31m"
        reset_color = "\033[0m"
        prompt_message = "Press Enter to continue..."
        if suggestion:
            row, col = suggestion
            suggested_move = row * Config.GRID["COLUMNS"] + col + 1
            message = f"{Config.MESSAGES['HELP']}{suggested_move}"
            print(f"{help_message_color}{message}{reset_color}")
        else:
            print(f"{no_move_color}No moves available.{reset_color}")
        input(prompt_message)

    def change_settings(self):
        self.display_settings_menu()
        while True:
            choice = input("Choose an option (1 -5): ").strip()
            if choice == "5":
                break
            self.process_setting_choice(choice)
            self.draw_interface()
            self.display_settings_menu()

    def display_settings_menu(self):
        title_color = "\033[1;33m"
        option_color = "\033[36m"
        reset_color = "\033[0m"
        separator = "\033[1;34m─" * 30 + "\033[0m"
        space = " " * 4
        title = f"{title_color}--- Settings Menu ---{reset_color}"
        options = [
            "1: Change Difficulty", "2: Toggle Statistics Display",
            "3: Toggle Commands Display", "4: Toggle Game Settings Display",
            "5: Return to Game"
        ]
        formatted_options = "\n".join(
            f"{space}{option_color}{option}{reset_color}"
            for option in options)
        print(f"\n{title}\n{separator}\n{formatted_options}\n{separator}")

    def process_setting_choice(self, choice):
        if choice == "1":
            self.change_difficulty()
        elif choice == "2":
            self.toggle_setting("show_stats")
        elif choice == "3":
            self.toggle_setting("show_commands")
        elif choice == "4":
            self.toggle_setting("show_game_settings")

    def change_difficulty(self):
        difficulties = ['easy', 'normal', 'hard']
        title_color = "\033[1;33m"
        choice_color = "\033[36m"
        success_color = "\033[32m"
        error_color = "\033[31m"
        reset_color = "\033[0m"
        checkmark = "\u2714"
        print(f"{title_color}Select difficulty:{reset_color}")
        for idx, difficulty in enumerate(difficulties, 1):
            print(
                f"  {choice_color}{idx}: {difficulty.capitalize()}{reset_color}"
            )
        while True:
            choice = input("Enter your choice (1-3): ").strip().lower()
            if choice.isdigit() and 1 <= int(choice) <= len(difficulties):
                new_difficulty = difficulties[int(choice) - 1]
                self.settings["difficulty"] = new_difficulty
                self.computer = ComputerPlayer(Config.PLAYERS["COMPUTER"],
                                               self.settings["difficulty"])
                message = (
                    f"{success_color}{checkmark} Difficulty: "
                    f"{self.settings['difficulty'].capitalize()}.{reset_color}\n"
                )
                print(message)
                break
            else:
                message = f"{error_color}Invalid choice. Try again... {reset_color}"
                print(message)
        input("Press Enter to return to settings...")

    def toggle_setting(self, setting):
        self.settings[setting] = not self.settings[setting]

    def draw_interface(self):
        self.clear_screen()
        self.display_title_bar()
        self.display_stats()
        self.board.display()

    def human_turn(self):
        move = self.get_human_input()
        if move == "help":
            self.provide_help()
            return False
        elif move == "settings":
            self.change_settings()
            return False
        elif self.validate_move(move):
            self.make_human_move(move)
            return True
        else:
            return False

    def get_human_input(self):
        prompt = "\033[1;34mEnter your move or command\n>>> \033[0m"
        return input(prompt).strip().lower()

    def validate_move(self, move):
        valid = False
        try:
            move = int(move) - 1
            row, column = divmod(move, Config.GRID["COLUMNS"])
            if not (0 <= move < Config.GRID["COLUMNS"]**2):
                print(Config.MESSAGES["BAD_MOVE"])
            elif isinstance(self.board.cells[row][column], str):
                print(Config.MESSAGES["FIELD_OCCUPIED"])
            else:
                valid = True
        except (ValueError, IndexError):
            print(Config.MESSAGES["BAD_MOVE"])
        if not valid:
            input("Press any key to try again")
        return valid

    def make_human_move(self, move):
        move = int(move) - 1
        row, column = divmod(move, Config.GRID["COLUMNS"])
        self.board.set_cell(row, column, self.human.symbol)

    def check_game_over(self):
        victor = self.board.check_victory_for(self.human.symbol) or \
                 self.board.check_victory_for(self.computer.symbol)

        if victor:
            return victor
        elif not self.board.get_free_fields():
            return 'tie'
        return None

    def display_end_game_message(self, outcome):
        self.draw_interface()
        terminal_width = shutil.get_terminal_size().columns

        win_message = "\U0001F389 Congratulations! You've won! \U0001F389"
        lose_message = "\U0001F61E Tough luck! You've lost. Try again! \U0001F61E"
        tie_message = "\U0001F642 It's a tie! Well played! \U0001F642"
        win_color = "\033[1;32m"
        lose_color = "\033[1;31m"
        tie_color = "\033[1;33m"
        reset_color = "\033[0m"

        if outcome == self.human.symbol:
            print(
                f"{win_color}{win_message.center(terminal_width)}{reset_color}"
            )
        elif outcome == self.computer.symbol:
            print(
                f"{lose_color}{lose_message.center(terminal_width)}{reset_color}"
            )
        else:
            print(
                f"{tie_color}{tie_message.center(terminal_width)}{reset_color}"
            )

    def update_stats(self, outcome):
        if outcome == self.human.symbol:
            self.stats["wins"] += 1
        elif outcome == self.computer.symbol:
            self.stats["losses"] += 1
        elif outcome == 'tie':
            self.stats["ties"] += 1

        self.display_end_game_message(outcome)

    def prompt_continue(self):
        print("\nGame Over. Play again?")
        user_input = input(">>> ").strip().lower()
        return user_input not in ["quit", "exit", "q", "n", "no"]

    def play(self):
        while True:
            self.reset_board()
            is_human_turn = True

            while self.board.get_free_fields():
                self.draw_interface()

                if is_human_turn:
                    if not self.human_turn():
                        continue
                else:
                    self.computer.make_move(self.board)

                victor = self.check_game_over()
                if victor:
                    self.update_stats(victor)
                    break
                is_human_turn = not is_human_turn

            if not self.prompt_continue():
                break


if __name__ == "__main__":
    game = Game()
    game.play()
