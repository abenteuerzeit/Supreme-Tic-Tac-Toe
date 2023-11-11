from config import Config
import shutil


class Board:

    def __init__(self):
        self.grid_settings = Config.GRID
        self.cols = self.grid_settings["COLUMNS"]
        self.cell_width = self.grid_settings["CELL_WIDTH"]
        self.terminal_width = shutil.get_terminal_size().columns
        self.reset()

    def reset(self):
        self.cells = [[self.cols * j + i + 1 for i in range(self.cols)]
                      for j in range(self.cols)]

    def center_line(self, content):
        padding_left = (self.terminal_width - self.get_board_width()) // 2
        return " " * padding_left + content

    def get_board_width(self):
        return self.cols * (self.cell_width + 1) + 1

    def display_row(self, row):
        row_content = "|" + "|".join(
            str(self.cells[row][col]).center(self.cell_width)
            for col in range(self.cols)) + "|"
        return self.center_line(row_content)

    def display(self):
        horizontal_line = "+" + "-" * self.cell_width
        padded_horizontal_line = self.center_line(horizontal_line *
                                                     self.cols + "+")
        empty_row = "|" + " " * self.cell_width

        print(padded_horizontal_line)
        for row in range(self.cols):
            print(self.center_line(empty_row * self.cols + "|"))
            print(self.display_row(row))
            print(self.center_line(empty_row * self.cols + "|"))
            print(padded_horizontal_line)

    def get_free_fields(self):
        return [(row, column) for row in range(self.cols)
                for column in range(self.cols)
                if not isinstance(self.cells[row][column], str)]

    def set_cell(self, row, column, value):
        self.cells[row][column] = value

    def check_victory_for(self, sgn):
        for rc in range(self.cols):
            if all(self.cells[rc][c] == sgn for c in range(self.cols)) or \
               all(self.cells[c][rc] == sgn for c in range(self.cols)):
                return sgn

        if all(self.cells[i][i] == sgn for i in range(self.cols)) or \
           all(self.cells[i][self.cols - 1 - i] == sgn for i in range(self.cols)):
            return sgn

        return None


if __name__ == "__main__":
    board = Board()
    board.display()
