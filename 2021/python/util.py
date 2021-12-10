HEADER = "\033[95m"
BLUE = "\033[94m"
CYAN = "\033[96m"
GREEN = "\033[92m"
YELLOW = "\033[93m"
RED = "\033[91m"
ENDC = "\033[0m"
BOLD = "\033[1m"
UNDERLINE = "\033[4m"


def print_header(*args):
    _print_color(args, HEADER)


def print_blue(*args):
    _print_color(args, BLUE)


def print_green(*args):
    _print_color(args, GREEN)


def print_red(*args):
    _print_color(args, RED)


def print_yellow(*args):
    _print_color(args, YELLOW)


def _print_color(args, color):
    if not args:
        print()

    args = list(args)
    args[0] = color + args[0]
    args[-1] = args[-1] + ENDC
    print(*args)
