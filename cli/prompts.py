from datetime import datetime
from colorama import Fore, Style

def read_nonempty(prompt: str) -> str:
    while True:
        val = input(prompt).strip()
        if val:
            return val
        print(Fore.RED + "Input cannot be empty." + Style.RESET_ALL)

def read_int(prompt: str) -> int:
    while True:
        s = input(prompt).strip()
        if s.isdigit():
            return int(s)
        print(Fore.RED + "Please enter a valid integer." + Style.RESET_ALL)

def read_datetime(prompt: str, fmt: str = "%Y-%m-%d %H:%M") -> datetime:
    while True:
        s = input(prompt + f" (format {fmt}): ").strip()
        try:
            return datetime.strptime(s, fmt)
        except ValueError:
            print(Fore.RED + "Invalid date/time format." + Style.RESET_ALL)

def confirm(prompt: str) -> bool:
    return input(prompt + " [y/N]: ").strip().lower() == "y"
