import time
import sys

color_codes = {
    "red": "\033[91m",
    "green": "\033[92m",
    "yellow": "\033[93m",
    "blue": "\033[94m",
    "orange": "\033[33m",
    "reset": "\033[0m"
}

RESET = "\033[0m"
RED = "\033[91m"
GREEN = "\033[92m"
YELLOW = "\033[93m"
BLUE = "\033[94m"
PURPLE = "\033[95m"
BROWN = "\033[38;5;94m"  # Not standard; uses 256-color mode

def color_text(text, color):
    return f"{color}{text}{RESET}"



def loading_bar(dot_count=3, delay=.5):
    for _ in range(dot_count):
        print(".", end="", flush=True)
        time.sleep(delay)
    print()  # Move to the next line afterward
    """ Usage:
print("Loading", end="", flush=True)
loading_bar() """