from colors import BWHITE, RESET, MAGHB


def print_map(map):
    for row in map:
        for e in row:
            print(e, end=' ')
        print()
    print()


def column(environment, index):
    return [row[index] for row in environment]


def get_key(dict, value):
    for key, val in dict.items():
        if val == value:
            return key


def print_with_title(title='INFO', message='Not implemented yet',
                     bg_color=MAGHB) -> None:
    print(f'{bg_color}{BWHITE}[{title}]{RESET}{BWHITE} {message}{RESET}')
