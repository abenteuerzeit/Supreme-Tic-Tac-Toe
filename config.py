class Config:
    GRID = {"COLUMNS": 3, "CELL_WIDTH": 7}
    PLAYERS = {"HUMAN": ":)", "COMPUTER": "PC"}
    MESSAGES = {
        "BAD_MOVE": "Bad move - repeat your input!",
        "FIELD_OCCUPIED": "Field already occupied - repeat your input!",
        "WIN": "You won!",
        "LOSE": "I won!",
        "TIE": "Tie!",
        "HELP": "Here's a suggested move: "
    }


def print_table(title, dictionary):
    max_key_length = max(len(key) for key in dictionary)
    max_value_length = max(len(str(value)) for value in dictionary.values())
    total_length = max_key_length + max_value_length + 1
    min_width = 15
    total_length = max(total_length, min_width)
    title_text = f"[ {title} ]"
    title_length = len(title_text)
    title_decorator = title_text + "=" * (total_length - title_length)
    decorator = "=" * total_length
    print(title_decorator)
    for key, value in dictionary.items():
        print(
            f"{key.ljust(max_key_length)}\t{str(value).ljust(max_value_length)}"
        )
    print(decorator)


if __name__ == "__main__":
    print("Configurations:")
    config = Config()
    for var in dir(config):
        if not var.startswith("__"):
            attr = getattr(config, var)
            print()
            if isinstance(attr, dict):
                print_table(var, attr)
            else:
                print(f"{var}: {attr}")
