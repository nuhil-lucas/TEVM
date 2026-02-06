from sys import exit as __exit__
from os import remove as __remove__
from os.path import exists as __exists__
from re import fullmatch as re_fullmatch
from typing import Callable
origin_input: Callable = input

def sys_exit(status: int = 0) -> None:
    __exit__(status)

def path_exists(path: str) -> bool:
    return __exists__(path)

def file_remove(path: str) -> None:
    if __exists__(path): __remove__(path)

def check_prjname(project_name: str):
    return bool(re_fullmatch(r'[A-Za-z0-9_]+', project_name))

def input(prompt: object = "", /) -> str | None:
    """
    Read a string from standard input. The trailing newline is stripped.

    The prompt string, if given, is printed to standard output without a trailing newline before reading input.

    If the user hits EOF (*nix: Ctrl-D, Windows: Ctrl-Z+Return), raise EOFError. On *nix systems, readline is used if available.

    It will exit whole program if EOFError or KeyboardInterrupt has been captured.
    """
    input_str: str = ""
    try:
        input_str: str = origin_input(prompt)
    except (EOFError, KeyboardInterrupt):
        sys_exit(0)
    else:
        return input_str

if __name__ == "__main__":
    pass