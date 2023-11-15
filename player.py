from config import Config
import random


class Player:

    def __init__(self, symbol):
        self.symbol = symbol

    def minimax(self, board, depth, is_maximizing, player_symbol):
        if board.check_victory_for(player_symbol):
            return 1 if player_symbol == self.symbol else -1
        if not board.get_free_fields():
            return 0

        best_score = float('-inf') if is_maximizing else float('inf')
        for row in range(Config.GRID["COLUMNS"]):
            for col in range(Config.GRID["COLUMNS"]):
                if isinstance(board.cells[row][col], int):
                    board.set_cell(row, col, player_symbol)
                    score = self.minimax(
                        board, depth + 1, not is_maximizing,
                        Config.PLAYERS["COMPUTER"]
                        if player_symbol == Config.PLAYERS["HUMAN"] else
                        Config.PLAYERS["HUMAN"])
                    board.set_cell(row, col,
                                   row * Config.GRID["COLUMNS"] + col + 1)
                    best_score = max(score,
                                     best_score) if is_maximizing else min(
                                         score, best_score)
        return best_score

    def get_minimax_move(self, board, player_symbol):
        best_score = float('-inf')
        best_move = None

        for row in range(Config.GRID["COLUMNS"]):
            for col in range(Config.GRID["COLUMNS"]):
                if isinstance(board.cells[row][col], int):
                    board.set_cell(row, col, player_symbol)
                    score = self.minimax(board, 0, False, player_symbol)
                    board.set_cell(row, col,
                                   row * Config.GRID["COLUMNS"] + col + 1)
                    if score > best_score:
                        best_score = score
                        best_move = (row, col)
        return best_move


class HumanPlayer(Player):

    def suggest_move(self, board):
        human_winning_move = self.find_winning_move(board,
                                                    Config.PLAYERS["HUMAN"])
        if human_winning_move:
            return human_winning_move

        computer_winning_move = self.find_winning_move(
            board, Config.PLAYERS["COMPUTER"])
        if computer_winning_move:
            return computer_winning_move

        return self.get_strategic_move(board)

    def find_winning_move(self, board, symbol):
        for row in range(Config.GRID["COLUMNS"]):
            for col in range(Config.GRID["COLUMNS"]):
                if isinstance(board.cells[row][col], int):
                    board.set_cell(row, col, symbol)
                    if board.check_victory_for(symbol):
                        board.set_cell(row, col,
                                       row * Config.GRID["COLUMNS"] + col + 1)
                        return (row, col)
                    board.set_cell(row, col,
                                   row * Config.GRID["COLUMNS"] + col + 1)
        return None

    def get_strategic_move(self, board):
        center = (Config.GRID["COLUMNS"] // 2, Config.GRID["COLUMNS"] // 2)
        corners = [(0, 0), (0, Config.GRID["COLUMNS"] - 1),
                   (Config.GRID["COLUMNS"] - 1, 0),
                   (Config.GRID["COLUMNS"] - 1, Config.GRID["COLUMNS"] - 1)]
        edges = [(0, 1), (1, 0), (1, 2), (2, 1)]

        if board.cells[center[0]][center[1]] not in [
                Config.PLAYERS["HUMAN"], Config.PLAYERS["COMPUTER"]
        ]:
            return center

        available_corners = [
            corner for corner in corners if board.cells[corner[0]][corner[1]]
            not in [Config.PLAYERS["HUMAN"], Config.PLAYERS["COMPUTER"]]
        ]
        if available_corners:
            return random.choice(available_corners)

        available_edges = [
            edge for edge in edges if board.cells[edge[0]][edge[1]] not in
            [Config.PLAYERS["HUMAN"], Config.PLAYERS["COMPUTER"]]
        ]
        if available_edges:
            return random.choice(available_edges)

        return random.choice(
            board.get_free_fields()) if board.get_free_fields() else None

    def make_move(self, board):
        is_valid_move = False
        while not is_valid_move:
            move = input("Enter your move: ")
            try:
                move = int(move)
                is_valid_move = 1 <= move <= Config.GRID["COLUMNS"]**2
            except ValueError:
                is_valid_move = False

            if not is_valid_move:
                print(Config.MESSAGES["BAD_MOVE"])
                continue

            move = int(move) - 1
            row, column = divmod(move, Config.GRID["COLUMNS"])
            if isinstance(board.cells[row][column], str):
                print(Config.MESSAGES["FIELD_OCCUPIED"])
                is_valid_move = False
                continue
            else:
                board.set_cell(row, column, self.symbol)
                break


class ComputerPlayer(Player):

    def __init__(self, symbol, difficulty='hard'):
        super().__init__(symbol)
        self.difficulty = difficulty

    def make_move(self, board):
        if self.difficulty == 'easy':
            self.make_random_move(board)
        elif self.difficulty == 'normal':
            if random.randint(0, 1) == 0:
                self.make_random_move(board)
            else:
                self.make_minimax_move(board)
        else:
            self.make_minimax_move(board)

    def make_random_move(self, board):
        free_fields = board.get_free_fields()
        if free_fields:
            move = random.choice(free_fields)
            board.set_cell(move[0], move[1], self.symbol)

    def make_minimax_move(self, board):
        best_move = self.get_minimax_move(board, self.symbol)
        if best_move:
            board.set_cell(best_move[0], best_move[1], self.symbol)
