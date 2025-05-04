from colors import BWHITE, RESET, MAGHB
from argparse import ArgumentTypeError


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


def check_positive(value):
    ivalue = int(value)
    if ivalue <= 0:
        raise ArgumentTypeError("%s is an invalid positive int value" % value)
    return ivalue


def print_inplace(title='INFO', message='Not implemented yet',
                  bg_color=MAGHB) -> None:
    print(f'{bg_color}{BWHITE}[{title}]{RESET}{BWHITE} {message}{RESET}\r',
          end='', flush=True)


def print_with_title(title='INFO', message='Not implemented yet',
                     bg_color=MAGHB, start_caracter='') -> None:
    print(f'{start_caracter}{bg_color}{BWHITE}[{title}]{RESET}{BWHITE} \
{message}{RESET}')
