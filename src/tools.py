from colors import CYANB, BWHITE, RESET

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

def print_info(message: str) -> None:
    print(f'{CYANB}{BWHITE}[INFO]{RESET}{BWHITE} {message}{RESET}')
